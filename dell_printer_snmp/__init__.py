"""Python wrapper for getting data from Dell printers via SNMP."""

from __future__ import annotations

import logging
from collections.abc import Generator, Iterable
from contextlib import suppress
from datetime import datetime, timedelta, timezone
from typing import Any, cast

import pysnmp.hlapi as hlapi
from pysnmp.error import PySnmpError
from pysnmp.entity.rfc3413.oneliner import cmdgen as lcd

from .const import (
    ATTR_COVER,
    ATTR_INPUT_TRAY,
    ATTR_OUTPUT_TRAY,
    ATTR_PAGE_DELIVERY,
    ATTR_STATUS,
    ATTR_MODEL,
    ATTR_PAGE_COUNT,
    ATTR_PRINTER_DETECTED_ERROR_STATE,
    ATTR_PRINTER_STATUS_PAPER,
    ATTR_PRINTER_STATUS_TONER,
    ATTR_SERIAL,
    ATTR_DEVICE_STATUS,
    ATTR_PRINTER_STATUS,
    ATTR_STATUS,
    ATTR_SUPPLIES,
    ATTR_TYPE,
    ATTR_UPTIME,
    COVER_MAP,
    COVERS_OIDS,
    OUTPUT_TYPE_MAP,
    PAGE_DELIVERY_MAP,
    SUBUNIT_STATUS_MAP,
    INPUT_TRAYS_OIDS,
    INPUT_TYPE_MAP,
    OIDS,
    OUTPUT_TRAYS_OIDS,
    PRINTER_STATUS_CRITICAL_MAP,
    PRINTER_STATUS_PAPER_MAP,
    PRINTER_STATUS_TONER_MAP,
    STATUS_MAP,
    SUPPLIES_OIDS,
    VAL_PRINTER_STATUS_PAPER_OK,
    VAL_PRINTER_STATUS_TONER_OK,
    VAL_STATUS_CRITICAL,
    VAL_STATUS_UNKNOWN,
)

_LOGGER = logging.getLogger(__name__)


class DictToObj(dict):
    """Dictionary to object class."""

    def __getattr__(self, name: str) -> Any:
        """Override __getattr__."""
        if name in self:
            return self[name]
        raise AttributeError("No such attribute: " + name)


class DellPrinterSnmp:
    """Main class to perform snmp requests to printer."""

    def __init__(
        self,
        host: str,
        port: int = 161,
        snmp_engine: hlapi.SnmpEngine = None,
        model: str | None = None,
    ) -> None:
        """Initialize."""
        if model:
            _LOGGER.debug("model: %s", model)

        self.model = None
        self.serial = None
        self._host = host
        self._port = port
        self._last_uptime: datetime | None = None
        self._snmp_engine = snmp_engine
        self._oids = tuple(self._iterate_oids(OIDS.values()))
        self._supplies_oids = tuple(self._iterate_oids(SUPPLIES_OIDS.values()))
        self._cover_oids = tuple(self._iterate_oids(COVERS_OIDS.values()))
        self._input_trays_oids = tuple(self._iterate_oids(INPUT_TRAYS_OIDS.values()))
        self._output_trays_oids = tuple(self._iterate_oids(OUTPUT_TRAYS_OIDS.values()))

        _LOGGER.debug("Using host: %s", host)

    async def async_update(self) -> DictToObj:
        """Update data from printer."""
        if not (raw_data := await self._get_data()):
            raise SnmpError("The printer did not return data")

        _LOGGER.debug("RAW data: %s", raw_data)

        data = DictToObj({})

        # get basic model and serial number information
        try:
            self.model = raw_data[OIDS[ATTR_MODEL]]
            data[ATTR_MODEL] = self.model
            self.serial = raw_data[OIDS[ATTR_SERIAL]]
            data[ATTR_SERIAL] = self.serial
        except (TypeError, AttributeError) as err:
            raise UnsupportedModel(
                "It seems that this printer model is not supported"
            ) from err

        # retrieve printer and device status
        try:
            printer_status = raw_data[OIDS[ATTR_PRINTER_STATUS]]
            data[ATTR_PRINTER_STATUS] = printer_status
            device_status = raw_data[OIDS[ATTR_DEVICE_STATUS]]
            data[ATTR_DEVICE_STATUS] = device_status
        except (AttributeError, TypeError):
            _LOGGER.debug("Incomplete data from printer")

        try:        
            data[ATTR_STATUS] = STATUS_MAP[device_status][printer_status]
        except (KeyError):
            _LOGGER.warn(f"Unknown status: device = {device_status}, printer = {printer_status}")
            data[ATTR_STATUS] = VAL_STATUS_UNKNOWN
        
        # retrieve status messages
        printer_error_message_raw = raw_data[OIDS[ATTR_PRINTER_DETECTED_ERROR_STATE]]
        printer_error_message_int = int.from_bytes(printer_error_message_raw.encode(), byteorder="big")

        # if machine is jammed, we can turn the critical status into something more specific
        if (data[ATTR_STATUS] == VAL_STATUS_CRITICAL):
            for critical_status in PRINTER_STATUS_CRITICAL_MAP:
                if printer_error_message_int & critical_status:
                    data[ATTR_STATUS] = PRINTER_STATUS_CRITICAL_MAP[critical_status]

        # get paper status
        data[ATTR_PRINTER_STATUS_PAPER] = VAL_PRINTER_STATUS_PAPER_OK
        for paper_status in PRINTER_STATUS_PAPER_MAP:
            if printer_error_message_int & paper_status:
                data[ATTR_PRINTER_STATUS_PAPER] = PRINTER_STATUS_PAPER_MAP[paper_status]
                break

        # get toner status
        data[ATTR_PRINTER_STATUS_TONER] = VAL_PRINTER_STATUS_TONER_OK
        for toner_status in PRINTER_STATUS_TONER_MAP:
            if printer_error_message_int & toner_status:
                data[ATTR_PRINTER_STATUS_TONER] = PRINTER_STATUS_TONER_MAP[toner_status]
                break

        # get uptime
        try:
            uptime = int(cast(str, raw_data.get(OIDS[ATTR_UPTIME]))) / 100
        except TypeError:
            pass
        else:
            if self._last_uptime:
                new_uptime = (datetime.utcnow() - timedelta(seconds=uptime)).replace(
                    microsecond=0, tzinfo=timezone.utc
                )
                if abs((new_uptime - self._last_uptime).total_seconds()) > 5:
                    data[ATTR_UPTIME] = self._last_uptime = new_uptime
                else:
                    data[ATTR_UPTIME] = self._last_uptime
            else:
                data[ATTR_UPTIME] = self._last_uptime = (
                    datetime.utcnow() - timedelta(seconds=uptime)
                ).replace(microsecond=0, tzinfo=timezone.utc)
        
        # get page count
        with suppress(ValueError):
            if not data.get(ATTR_PAGE_COUNT) and raw_data.get(OIDS[ATTR_PAGE_COUNT]):
                data[ATTR_PAGE_COUNT] = int(
                    cast(str, raw_data.get(OIDS[ATTR_PAGE_COUNT]))
                )

        _LOGGER.debug("Data: %s", data)

        # get supplies
        if not (raw_data_table := await self._get_data_table(self._supplies_oids)):
            raise SnmpError("The printer did not return data")

        _LOGGER.debug("RAW data table: %s", raw_data_table)
       
        data_table = []
        for cover in raw_data_table:
            data_item = {}
            for oid, value in cover.items():
                for attr in SUPPLIES_OIDS.keys():
                    if oid.startswith(SUPPLIES_OIDS[attr] + "."):
                        data_item[attr] = str(value)
            data_table.append(data_item)
            
        data[ATTR_SUPPLIES] = data_table

        # get covers
        if not (raw_data_table := await self._get_data_table(self._cover_oids)):
            raise SnmpError("The printer did not return data")

        _LOGGER.debug("RAW data table: %s", raw_data_table)
       
        data_table = []
        for cover in raw_data_table:
            data_item = {}
            for oid, value in cover.items():
                value = str(value)
                for attr in COVERS_OIDS.keys():
                    if oid.startswith(COVERS_OIDS[attr] + "."):
                        if attr == ATTR_STATUS:
                            data_item[attr] = COVER_MAP[value]
                        else:
                            data_item[attr] = value
            data_table.append(data_item)
            
        data[ATTR_COVER] = data_table

        # get input trays
        if not (raw_data_table := await self._get_data_table(self._input_trays_oids)):
            raise SnmpError("The printer did not return data")

        _LOGGER.debug("RAW data table: %s", raw_data_table)
       
        data_table = []
        for input_tray in raw_data_table:
            data_item = {}
            for oid, value in input_tray.items():
                value = str(value)
                for attr in INPUT_TRAYS_OIDS.keys():
                    if oid.startswith(INPUT_TRAYS_OIDS[attr] + "."):
                        if attr == ATTR_TYPE:
                            data_item[attr] = INPUT_TYPE_MAP[value]
                        elif attr == ATTR_STATUS:
                            if value not in SUBUNIT_STATUS_MAP.keys():
                                # go to the next smallest power of 2
                                value = str(1<<(int(value)-1).bit_length())
                            data_item[attr] = SUBUNIT_STATUS_MAP[value]
                        else:
                            data_item[attr] = value
            data_table.append(data_item)
            
        data[ATTR_OUTPUT_TRAY] = data_table

        # get output trays
        if not (raw_data_table := await self._get_data_table(self._output_trays_oids)):
            raise SnmpError("The printer did not return data")

        _LOGGER.debug("RAW data table: %s", raw_data_table)
       
        data_table = []
        for output_tray in raw_data_table:
            data_item = {}
            for oid, value in output_tray.items():
                value = str(value)
                for attr in OUTPUT_TRAYS_OIDS.keys():
                    if oid.startswith(OUTPUT_TRAYS_OIDS[attr] + "."):
                        if attr == ATTR_TYPE:
                            data_item[attr] = OUTPUT_TYPE_MAP[value]
                        elif attr == ATTR_STATUS:
                            if value not in SUBUNIT_STATUS_MAP.keys():
                                # go to the next smallest power of 2
                                value = str(1<<(int(value)-1).bit_length())
                            data_item[attr] = SUBUNIT_STATUS_MAP[value]
                        elif attr == ATTR_PAGE_DELIVERY:
                            data_item[attr] = PAGE_DELIVERY_MAP[value]
                        else:
                            data_item[attr] = value
            data_table.append(data_item)
            
        data[ATTR_INPUT_TRAY] = data_table
        return data


    async def _get_data(self) -> dict[str, Any]:
        """Retrieve data from printer."""
        raw_data = {}

        if not self._snmp_engine:
            self._snmp_engine = hlapi.SnmpEngine()

        try:
            request_args = [
                self._snmp_engine,
                hlapi.CommunityData("public", mpModel=0),
                hlapi.UdpTransportTarget(
                    (self._host, self._port), timeout=2, retries=10
                ),
                hlapi.ContextData(),
            ]
            errindication, errstatus, errindex, restable = next(hlapi.getCmd(
                *request_args, *self._oids,
            ))
        except PySnmpError as err:
            raise ConnectionError(err) from err
        if errindication:
            raise SnmpError(errindication)
        if errstatus:
            raise SnmpError(f"{errstatus}, {errindex}")

        for resrow in restable:
            raw_data[str(resrow[0])] = str(resrow[-1])
        return raw_data


    async def _get_data_table(self, oids) -> list[dict[str, Any]]:
        """Retrieve data from printer."""
        raw_data = {}

        if not self._snmp_engine:
            self._snmp_engine = hlapi.SnmpEngine()

        try:
            request_args = [
                self._snmp_engine,
                hlapi.CommunityData("public", mpModel=0),
                hlapi.UdpTransportTarget(
                    (self._host, self._port), timeout=2, retries=10
                ),
                hlapi.ContextData(),
            ]

            iterator = hlapi.nextCmd(
                *request_args,
                *oids,
                lexicographicMode=False
            )
        except PySnmpError as err:
            raise ConnectionError(err) from err

        data = []

        for errindication, errstatus, errindex, varBinds in iterator:

            result = {}
            if errindication:
                raise SnmpError(errindication)
            elif errstatus:
                raise SnmpError(f"{errstatus}, {errindex}")
            else:
                for varBind in varBinds:
                    result.update([(str(varBind[0]), varBind[-1])])
            data.append(result)

        return data


    @classmethod
    def _iterate_oids(cls, oids: Iterable) -> Generator:
        """Iterate OIDS to retrieve from printer."""
        for oid in oids:
            yield hlapi.ObjectType(hlapi.ObjectIdentity(oid))


class SnmpError(Exception):
    """Raised when SNMP request ended in error."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status


class UnsupportedModel(Exception):
    """Raised when no model, serial no data."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status

[![GitHub Release][releases-shield]][releases]


# dell-printer-snmp
Python wrapper for getting data from Dell printers via snmp

## How to use package
```py
import asyncio
import logging
from sys import argv

import pysnmp.hlapi as hlapi

from dell_printer_snmp import DellPrinterSnmp, SnmpError, UnsupportedModel

# printer IP address/hostname
HOST = "192.168.0.20"
logging.basicConfig(level=logging.INFO)


async def main():
    host = argv[1] if len(argv) > 1 else HOST

    external_snmp = False
    if len(argv) > 3 and argv[2] == "use_external_snmp":
        external_snmp = True

    if external_snmp:
        print("Using external SNMP engine")
        snmp_engine = hlapi.SnmpEngine()
        dell_printer = DellPrinterSnmp(host, snmp_engine=snmp_engine)
    else:
        dell_printer = DellPrinterSnmp(host)

    try:
        data = await dell_printer.async_update()
    except (ConnectionError, SnmpError, UnsupportedModel) as error:
        print(f"{error}")
        exit()

    print(f"Model: {dell_printer.model}")
    if data:
        print(f"Status: {data.status}")
        print(f"Serial no: {data.serial}")
        print(f"Page counter: {data.page_counter}")
        print(f"Sensors data: {data}")


loop = asyncio.get_event_loop_policy().get_event_loop()
loop.run_until_complete(main())
```

[releases]: https://github.com/kongo09/dell-printer-snmp/releases
[releases-shield]: https://img.shields.io/github/release/kongo09/dell-printer-snmp.svg?style=popout

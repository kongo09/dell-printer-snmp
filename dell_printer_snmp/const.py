"""Constants for Dell Printer SNMP library."""

from typing import Final

ATTR_COUNTERS: Final[str] = "counters"
ATTR_MODEL: Final[str] = "model"
ATTR_PAGE_COUNT: Final[str] = "page_counter"
ATTR_SERIAL: Final[str] = "serial"
ATTR_PRINTER_STATUS: Final[str] = "printer_status"
ATTR_DEVICE_STATUS: Final[str] = "device_status"
ATTR_PRINTER_DETECTED_ERROR_STATE: Final[str] = "printer_detected_error_state"
ATTR_PRINTER_STATUS_PAPER: Final[str] = "printer_status_paper"
ATTR_PRINTER_STATUS_TONER: Final[str] = "printer_status_toner"
ATTR_STATUS: Final[str] = "status"
ATTR_UPTIME: Final[str] = "uptime"
ATTR_NAME: Final[str] = "name"
ATTR_SUPPLIES: Final[str] = "supplies"
ATTR_COLOR: Final[str] = "color"
ATTR_CAPACITY: Final[str] = "capacity"
ATTR_LEVEL: Final[str] = "level"
ATTR_COVER: Final[str] = "cover"
ATTR_TRAY: Final[str] = "tray"
ATTR_INPUT_TRAY: Final[str] = "input_tray"
ATTR_OUTPUT_TRAY: Final[str] = "output_tray"
ATTR_TYPE: Final[str] = "type"
ATTR_MEDIA: Final[str] = "media"
ATTR_PAGE_DELIVERY: Final[str] = "page_delivery"

VAL_STATUS_UNKNOWN: Final[str] = "unknown"
VAL_STATUS_STANDBY: Final[str] = "standby"
VAL_STATUS_IDLE: Final[str] = "idle"
VAL_STATUS_PRINTING: Final[str] = "printing"
VAL_STATUS_WARNING: Final[str] = "warning"
VAL_STATUS_CRITICAL: Final[str] = "critical"
VAL_STATUS_WARMUP: Final[str] = "warmup"
VAL_STATUS_UNAVAILABLE: Final[str] = "unavailable"

VAL_PRINTER_STATUS_JAMMED: Final[str] = "jammed"
VAL_PRINTER_STATUS_OPENDOOR: Final[str] = "open_door"

VAL_PRINTER_STATUS_PAPER_OK: Final[str] = "ok"
VAL_PRINTER_STATUS_PAPER_LOW: Final[str] = "low"
VAL_PRINTER_STATUS_PAPER_EMPTY: Final[str] = "empty"

VAL_PRINTER_STATUS_TONER_OK: Final[str] = "ok"
VAL_PRINTER_STATUS_TONER_LOW: Final[str] = "low"
VAL_PRINTER_STATUS_TONER_EMPTY: Final[str] = "empty"

VAL_OTHER: Final[str] = "other"
VAL_OPEN: Final[str] = "open"
VAL_CLOSED: Final[str] = "closed"

VAL_ACTIVE: Final[str] = "active"
VAL_BUSY: Final[str] = "busy"

VAL_UNKNOWN: Final[str] = "unknown"
VAL_SHEETFEED_AUTO_REMOVABLE: Final[str] = "removable auto sheet feeder"
VAL_SHEETFEED_AUTO_NONREMOVABLE: Final[str] = "unremovable auto sheet feeder"
VAL_SHEETFEED_MANUAL: Final[str] = "manual sheet feeder"
VAL_CONT_ROLL: Final[str] = "continuous roll"
VAL_CONT_FAN_ROLL: Final[str] = "continous fan-roll"
VAL_REMOVABLE_BIN: Final[str] = "removable bin"
VAL_UNREMOVABLE_BIN: Final[str] = "unremovable bin"
VAL_MAILBOX: Final[str] = "mailbox"
VAL_CONT_FAN_FOLD: Final[str] = "continous fan-fold"
VAL_FACE_UP: Final[str] = "face up"
VAL_FACE_DOWN: Final[str] = "face down"

OIDS: Final[dict[str, str]] = {
    ATTR_MODEL: "1.3.6.1.2.1.1.1.0",
    ATTR_PAGE_COUNT: "1.3.6.1.2.1.43.10.2.1.4.1.1",
    ATTR_SERIAL: "1.3.6.1.2.1.43.5.1.1.17.1",
    ATTR_PRINTER_STATUS: "1.3.6.1.2.1.25.3.5.1.1.1",
    ATTR_DEVICE_STATUS: "1.3.6.1.2.1.25.3.2.1.5.1",
    ATTR_PRINTER_DETECTED_ERROR_STATE: "1.3.6.1.2.1.25.3.5.1.2.1",
    ATTR_UPTIME: "1.3.6.1.2.1.1.3.0",
}

SUPPLIES_OIDS: Final[dict[str, str]] = {
    ATTR_NAME: "1.3.6.1.2.1.43.11.1.1.6.1",
    ATTR_COLOR: "1.3.6.1.2.1.43.12.1.1.4",
    ATTR_CAPACITY: "1.3.6.1.2.1.43.11.1.1.8",
    ATTR_LEVEL: "1.3.6.1.2.1.43.11.1.1.9",
}

COVERS_OIDS: Final[dict[str, str]] = {
    ATTR_NAME: "1.3.6.1.2.1.43.6.1.1.2",
    ATTR_STATUS: "1.3.6.1.2.1.43.6.1.1.3",
}

INPUT_TRAYS_OIDS: Final[dict[str, str]] = {
    ATTR_NAME: "1.3.6.1.2.1.43.8.2.1.13",
    ATTR_TYPE: "1.3.6.1.2.1.43.8.2.1.2",
    ATTR_CAPACITY: "1.3.6.1.2.1.43.8.2.1.9",
    ATTR_STATUS: "1.3.6.1.2.1.43.8.2.1.11",
    ATTR_MEDIA: "1.3.6.1.2.1.43.8.2.1.21",
}

OUTPUT_TRAYS_OIDS: Final[dict[str, str]] = {
    ATTR_NAME: "1.3.6.1.2.1.43.9.2.1.7",
    ATTR_TYPE: "1.3.6.1.2.1.43.9.2.1.2",
    ATTR_CAPACITY: "1.3.6.1.2.1.43.9.2.1.4",
    ATTR_STATUS: "1.3.6.1.2.1.43.9.2.1.6",
    ATTR_PAGE_DELIVERY: "1.3.6.1.2.1.43.9.2.1.20",
}

STATUS_MAP: Final[dict[str, dict[str, str]]] = {
    "2": {
        "1": VAL_STATUS_STANDBY,
        "3": VAL_STATUS_IDLE,
        "4": VAL_STATUS_PRINTING,
        "5": VAL_STATUS_WARMUP,
    },
    "3": {
        "3": VAL_STATUS_WARNING,
        "4": VAL_STATUS_WARNING,
    },
    "5": {
        "1": VAL_STATUS_CRITICAL,
        "5": VAL_STATUS_WARMUP,
    }
}

COVER_MAP: Final[dict[str, str]] = {
    "1": VAL_OTHER,
    "3": VAL_OPEN,
    "4": VAL_CLOSED,
    "5": VAL_OPEN,
    "6": VAL_CLOSED,
}

TRAY_STATUS_MAP: Final[dict[str, str]] = {
    "0": VAL_STATUS_IDLE,
    "3": VAL_STATUS_CRITICAL,
    "4": VAL_ACTIVE,
    "6": VAL_BUSY,
    "16": VAL_STATUS_CRITICAL,
}

INPUT_TYPE_MAP: Final[dict[str, str]] = {
    "1": VAL_OTHER,
    "2": VAL_UNKNOWN,
    "3": VAL_SHEETFEED_AUTO_REMOVABLE,
    "4": VAL_SHEETFEED_AUTO_NONREMOVABLE,
    "5": VAL_SHEETFEED_MANUAL,
    "6": VAL_CONT_ROLL,
    "7": VAL_CONT_FAN_ROLL,
}

SUBUNIT_STATUS_MAP: Final[dict[int, str]] = {
    "0": VAL_STATUS_IDLE,
    "1": VAL_STATUS_UNAVAILABLE,
    "2": VAL_STATUS_STANDBY,
    "3": VAL_STATUS_UNAVAILABLE,
    "4": VAL_ACTIVE,
    "5": VAL_UNKNOWN,
    "6": VAL_BUSY,
    "7": VAL_UNKNOWN,
    "8": VAL_STATUS_WARNING,
    "16": VAL_STATUS_CRITICAL,
    "64": VAL_STATUS_UNKNOWN,
}

OUTPUT_TYPE_MAP: Final[dict[str, str]] = {
    "1": VAL_OTHER,
    "2": VAL_UNKNOWN,
    "3": VAL_REMOVABLE_BIN,
    "4": VAL_UNREMOVABLE_BIN,
    "5": VAL_CONT_ROLL,
    "6": VAL_MAILBOX,
    "7": VAL_CONT_FAN_FOLD,
}

PAGE_DELIVERY_MAP: Final[dict[str, str]] = {
    "3": VAL_FACE_UP,
    "4": VAL_FACE_DOWN,
}

PRINTER_STATUS_PAPER_MAP: Final[dict[int, str]] = {
    0b00000000: VAL_PRINTER_STATUS_PAPER_OK,
    0b10000000: VAL_PRINTER_STATUS_PAPER_LOW,
    0b01000000: VAL_PRINTER_STATUS_PAPER_EMPTY,
}

PRINTER_STATUS_TONER_MAP: Final[dict[int, str]] = {
    0b00000000: VAL_PRINTER_STATUS_TONER_OK,
    0b00100000: VAL_PRINTER_STATUS_TONER_LOW,
    0b00010000: VAL_PRINTER_STATUS_TONER_EMPTY,
}

PRINTER_STATUS_CRITICAL_MAP: Final[dict[int, str]] = {
    0b00001000: VAL_PRINTER_STATUS_OPENDOOR,
    0b00000100: VAL_PRINTER_STATUS_JAMMED,
}

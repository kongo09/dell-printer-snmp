from __future__ import annotations

import asyncio
from typing import Any

import pysnmp.hlapi as hlapi


class DellPrinterSnmp:
    """Main class to perform snmp requests to printer."""

    async def _get_data_table(self, oids) -> dict[str, Any]:

        iterator = hlapi.nextCmd(
            hlapi.SnmpEngine(),
            hlapi.CommunityData('public', mpModel=0),
            hlapi.UdpTransportTarget(('192.168.0.20', 161)),
            hlapi.ContextData(),
            *oids,
            lexicographicMode=False
        )

        result = {}

        for errorIndication, errorStatus, errorIndex, varBinds in iterator:

            if errorIndication:
                print(errorIndication)
                break

            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
                break

            else:
                for varBind in varBinds:
                    result.update([(str(varBind[0]), str(varBind[-1]))])

        return result


async def main():
    oids = (
        hlapi.ObjectType(hlapi.ObjectIdentity('1.3.6.1.2.1.43.11.1.1.6')),
        hlapi.ObjectType(hlapi.ObjectIdentity('1.3.6.1.2.1.43.11.1.1.8')),
        hlapi.ObjectType(hlapi.ObjectIdentity('1.3.6.1.2.1.43.11.1.1.9')),
        hlapi.ObjectType(hlapi.ObjectIdentity('1.3.6.1.2.1.43.12.1.1.4')),
    )
    dps = DellPrinterSnmp()
    result = await dps._get_data_table(oids)

    for k,v in result.items():
        print(f"{k} = {v}")
        


loop = asyncio.get_event_loop_policy().get_event_loop()
loop.run_until_complete(main())
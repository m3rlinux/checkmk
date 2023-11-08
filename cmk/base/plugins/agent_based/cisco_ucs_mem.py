#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from dataclasses import dataclass
from enum import Enum

from cmk.base.plugins.agent_based.agent_based_api.v1 import register, SNMPTree

from .agent_based_api.v1 import State
from .agent_based_api.v1.type_defs import StringTable
from .utils.cisco_ucs import DETECT, Operability, Presence


class MemoryType(Enum):
    undiscovered = "0"
    other = "1"
    unknown = "2"
    dram = "3"
    edram = "4"
    vram = "5"
    sram = "6"
    ram = "7"
    rom = "8"
    flash = "9"
    eeprom = "10"
    feprom = "11"
    eprom = "12"
    cdram = "13"
    n3DRAM = "14"
    sdram = "15"
    sgram = "16"
    rdram = "17"
    ddr = "18"
    ddr2 = "19"
    ddr2FbDimm = "20"
    ddr3 = "24"
    fbd2 = "25"
    ddr4 = "26"

    def monitoring_state(self) -> State:
        return State.OK


@dataclass(frozen=True, kw_only=True)
class MemoryModule:
    serial: str
    capacity: str
    memtype: MemoryType
    operability: Operability
    presence: Presence


def parse_cisco_ucs_mem(string_table: StringTable) -> dict[str, MemoryModule]:
    return {
        name: MemoryModule(
            serial=serial,
            capacity=capacity,
            memtype=MemoryType(memtype),
            operability=Operability(operability),
            presence=Presence(presence),
        )
        for name, serial, memtype, capacity, operability, presence in string_table
    }


register.snmp_section(
    name="cisco_ucs_mem",
    parse_function=parse_cisco_ucs_mem,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9.9.719.1.30.11.1",
        oids=[
            "3",  # .1.3.6.1.4.1.9.9.719.1.30.11.1.3  cucsMemoryUnitRn
            "19",  # .1.3.6.1.4.1.9.9.719.1.30.11.1.19 cucsMemoryUnitSerial
            "23",  # .1.3.6.1.4.1.9.9.719.1.30.11.1.23 cucsMemoryUnitType
            "6",  # .1.3.6.1.4.1.9.9.719.1.30.11.1.6  cucsMemoryUnitCapacity
            "14",  # .1.3.6.1.4.1.9.9.719.1.30.11.1.14 cucsMemoryUnitOperability
            "17",  # .1.3.6.1.4.1.9.9.719.1.30.11.1.17 cucsMemoryUnitPresence
        ],
    ),
    detect=DETECT,
)

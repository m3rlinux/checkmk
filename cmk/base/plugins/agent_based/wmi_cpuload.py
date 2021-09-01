#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from typing import NamedTuple, Optional

from .agent_based_api.v1 import get_average, get_value_store, register, Service
from .agent_based_api.v1.type_defs import CheckResult, DiscoveryResult, StringTable
from .utils.cpu import Load, ProcessorType
from .utils.cpu import Section as CPUSection
from .utils.cpu_load import check_cpu_load, CPULoadParams
from .utils.wmi import get_wmi_time, parse_wmi_table, required_tables_missing, WMIQueryTimeoutError


class Section(NamedTuple):
    load: float
    timestamp: float
    processor_type: ProcessorType
    n_cores: int


def parse_wmi_cpuload(string_table: StringTable) -> Optional[Section]:
    wmi_tables = parse_wmi_table(string_table)
    if required_tables_missing(
            wmi_tables,
        [
            "computer_system",
            "system_perf",
        ],
    ):
        return None

    try:
        load = wmi_tables["system_perf"].get(0, "ProcessorQueueLength")
        timestamp = get_wmi_time(wmi_tables["system_perf"], 0)
        computer_system = wmi_tables["computer_system"]
    except (KeyError, WMIQueryTimeoutError):
        return None
    assert load

    try:
        n_cores = computer_system.get(0, "NumberOfLogicalProcessors")
        processor_type = ProcessorType.logical
    except (KeyError, WMIQueryTimeoutError):
        try:
            n_cores = computer_system.get(0, "NumberOfProcessors")
            processor_type = ProcessorType.physical
        except (KeyError, WMIQueryTimeoutError):
            return None

    # NumberOfLogicalProcessors can be an empty string, not sure why
    if not n_cores:
        return None

    return Section(
        int(load),
        timestamp,
        processor_type,
        int(n_cores),
    )


register.agent_section(
    name="wmi_cpuload",
    parse_function=parse_wmi_cpuload,
)


def discover_wmi_cpuload(section: Section) -> DiscoveryResult:
    yield Service()


def check_wmi_cpuload(
    params: CPULoadParams,
    section: Section,
) -> CheckResult:
    yield from check_cpu_load(
        params,
        CPUSection(
            Load(
                section.load,
                get_average(
                    get_value_store(),
                    "load_5min",
                    section.timestamp,
                    section.load,
                    5,
                ),
                get_average(
                    get_value_store(),
                    "load_15min",
                    section.timestamp,
                    section.load,
                    15,
                ),
            ),
            section.n_cores,
            0,
            type=section.processor_type,
        ),
    )


register.check_plugin(
    name="wmi_cpuload",
    discovery_function=discover_wmi_cpuload,
    check_function=check_wmi_cpuload,
    service_name="Processor Queue",
    check_default_parameters={},
    check_ruleset_name="cpu_load",
)

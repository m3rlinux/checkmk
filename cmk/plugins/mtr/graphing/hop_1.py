#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.graphing.v1 import graphs, metrics, perfometers, Title

UNIT_TIME = metrics.Unit(metrics.TimeNotation())
UNIT_PERCENTAGE = metrics.Unit(metrics.DecimalNotation("%"))

metric_hop_1_rta = metrics.Metric(
    name="hop_1_rta",
    title=Title("Hop 1 round trip average"),
    unit=UNIT_TIME,
    color=metrics.Color.ORANGE,
)
metric_hop_1_rtmax = metrics.Metric(
    name="hop_1_rtmax",
    title=Title("Hop 1 round trip maximum"),
    unit=UNIT_TIME,
    color=metrics.Color.BLUE,
)
metric_hop_1_rtmin = metrics.Metric(
    name="hop_1_rtmin",
    title=Title("Hop 1 round trip minimum"),
    unit=UNIT_TIME,
    color=metrics.Color.GREEN,
)
metric_hop_1_rtstddev = metrics.Metric(
    name="hop_1_rtstddev",
    title=Title("Hop 1 round trip standard devation"),
    unit=UNIT_TIME,
    color=metrics.Color.PINK,
)
metric_hop_1_pl = metrics.Metric(
    name="hop_1_pl",
    title=Title("Hop 1 packet loss"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.BROWN,
)

perfometer_hop_1_pl_hop_1_rta = perfometers.Bidirectional(
    name="hop_1_pl_hop_1_rta",
    left=perfometers.Perfometer(
        name="hop_1_pl",
        focus_range=perfometers.FocusRange(
            perfometers.Closed(0),
            perfometers.Closed(100.0),
        ),
        segments=["hop_1_pl"],
    ),
    right=perfometers.Perfometer(
        name="hop_1_rta",
        focus_range=perfometers.FocusRange(
            perfometers.Closed(0),
            perfometers.Open(1),
        ),
        segments=["hop_1_rta"],
    ),
)

graph_hop_1_round_trip_average = graphs.Graph(
    name="hop_1_round_trip_average",
    title=Title("Hop 1 round trip average"),
    simple_lines=[
        "hop_1_rtmax",
        "hop_1_rtmin",
        "hop_1_rta",
        "hop_1_rtstddev",
    ],
)
graph_hop_1_packet_loss = graphs.Graph(
    name="hop_1_packet_loss",
    title=Title("Hop 1 packet loss"),
    compound_lines=["hop_1_pl"],
)

#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from pytest_mock import MockerFixture

from cmk.utils.notify_types import EventRule, NotificationRuleID

from cmk.gui.wato.pages.notifications.migrate import (
    migrate_to_event_rule,
    migrate_to_notification_quick_setup_spec,
)
from cmk.gui.wato.pages.notifications.quick_setup_types import NotificationQuickSetupSpec

QUICK_SETUP_PARAMS: NotificationQuickSetupSpec = {
    "triggering_events": {
        "host_events": [
            ("status_change", (-1, 0)),
            ("status_change", (1, 2)),
            ("flapping_state", None),
            ("acknowledgement", None),
            ("alert_handler", "failure"),
        ],
        "service_events": [
            ("status_change", (-1, 0)),
            ("status_change", (1, 2)),
            ("status_change", (3, 0)),
            ("downtime", None),
            ("alert_handler", "success"),
        ],
    },
    "filter_for_hosts_and_services": {
        "host_filters": {},
        "service_filters": {},
        "assignee_filters": {},
        "general_filters": {},
        "ec_alert_filters": {},
    },
    "notification_method": {
        "method": ("mail", object),
        "notification_effect": object,
    },
    "recipient": [
        ("all_contacts_affected", None),
    ],
    "sending_conditions": {
        "frequency_and_timing": {
            "restrict_timeperiod": "24X7",
            "limit_by_count": (2, 4),
            "throttle_periodic": (3, 5),
        },
        "content_based_filtering": {
            "by_plugin_output": "some_plugin_output",
            "custom_by_comment": "some_comment",
        },
    },
    "general_properties": {
        "description": "foo",
        "settings": {
            "disable_rule": None,
            "allow_users_to_disable": None,
        },
        "comment": "foo.comment",
        "documentation_url": "foo.com",
    },
}

EVENT_RULE_PARAMS: EventRule = EventRule(
    rule_id=NotificationRuleID("uuid4_rule_id"),
    match_host_event=["?r", "du", "f", "x", "af"],
    match_service_event=["?r", "wc", "ur", "s", "as"],
    notify_plugin=("mail", None),
    match_escalation=(2, 4),
    match_escalation_throttle=(3, 5),
    match_timeperiod="24X7",
    match_plugin_output="some_plugin_output",
    match_notification_comment="some_comment",
    contact_all=False,
    contact_all_with_email=False,
    contact_object=False,
    match_ec=False,
    disabled=True,
    allow_disable=True,
    description="foo",
    docu_url="foo.com",
    comment="foo.comment",
)


def test_quick_setup_notifications_transform_to_disk(mocker: MockerFixture) -> None:
    mocker.patch("cmk.gui.wato.pages.notifications.migrate.uuid4", return_value="uuid4_rule_id")
    assert migrate_to_event_rule(QUICK_SETUP_PARAMS) == EVENT_RULE_PARAMS


def test_quick_setup_notifications_transform_to_frontend() -> None:
    assert migrate_to_notification_quick_setup_spec(EVENT_RULE_PARAMS) == QUICK_SETUP_PARAMS

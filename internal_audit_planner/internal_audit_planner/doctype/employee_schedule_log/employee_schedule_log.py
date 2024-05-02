# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json


class EmployeeScheduleLog(Document):
    pass


@frappe.whitelist()
def check_employee_schedules(
    filters=None, or_filters=None
):
    schedule_log = frappe.get_list(
        "Employee Schedule Log", filters=filters, fields=["*"],
    )

    if schedule_log:
        if schedule_log[0].type == "Leave":
            frappe.throw("This Employee is on leave on that date")
        elif schedule_log[0].type == "Planned":
            frappe.throw("This Employee has an Audit Planned schudule at that time")
        elif schedule_log[0].type == "Actual":
            frappe.throw("This Employee Attend an Actual Audit at that time")


@frappe.whitelist()
def get_events(doctype, start, end, field_map, filters=None):
    field_map = frappe._dict(json.loads(field_map))

    filters = json.loads(filters) if filters else []

    start_date = "ifnull(%s, '0001-01-01 00:00:00')" % field_map.start
    end_date = "ifnull(%s, '2199-12-31 00:00:00')" % field_map.end

    filters += [
        [doctype, start_date, "<=", end],
        [doctype, end_date, ">=", start],
    ]

    custom_order = "FIELD(type, 'Leave', 'Planned', 'Actual')"

    events = frappe.get_list(
        doctype, fields=["*"], filters=filters, order_by=custom_order
    )

    for event in events:
        employee = frappe.get_doc("Company Employee", event.employee)
        if event.type == "Leave":
            event.color = "#FC6149"
            event.subject = f"{employee.full_name} On Leave"
        elif event.type == "Planned":
            event.color = "#F5A91B"
            event.subject = f"{employee.full_name} has an Audit Planned"
        elif event.type == "Actual":
            event.color = "#6495ED"
            event.subject = f"{employee.full_name} Attend an Actual Audit"
        event.all_day = 0
    return events

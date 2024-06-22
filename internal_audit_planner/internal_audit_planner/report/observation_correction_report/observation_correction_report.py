# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta


def execute(filters=None):
    columns = get_columns()

    base_query = """
        SELECT
            obs.*,
            auditor_emp.full_name AS auditor_name,
            auditee_hod_emp.full_name AS auditee_hod_name,
            responsible_emp.full_name AS responsible_person_name
        FROM
            `tabObservation Correction` AS obs
        LEFT JOIN
            `tabCompany Employee` AS auditor_emp ON obs.auditor = auditor_emp.name
        LEFT JOIN
            `tabCompany Employee` AS auditee_hod_emp ON obs.auditee_hod = auditee_hod_emp.name
        LEFT JOIN
            `tabCompany Employee` AS responsible_emp ON obs.responsible_person = responsible_emp.name
        WHERE
            1=1
    """

    filter_conditions = []
    filter_values = []

    if filters:
        if "internal_audit_conformity" in filters:
            filter_conditions.append("internal_audit_conformity = %s")
            filter_values.append(filters["internal_audit_conformity"])

        if "internal_audit_plan" in filters:
            filter_conditions.append("internal_audit_plan = %s")
            filter_values.append(filters["internal_audit_plan"])

        if "from_date" in filters and "to_date" in filters:
            filter_conditions.append("obs.date BETWEEN %s AND %s")
            filter_values.append(filters["from_date"])
            filter_values.append(filters["to_date"])
        elif "from_date" in filters:
            filter_conditions.append("obs.date >= %s")
            filter_values.append(filters["from_date"])
        elif "to_date" in filters:
            to_date_end_of_day = datetime.strptime(filters["to_date"], '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
            filter_conditions.append("obs.date <= %s")
            filter_values.append(to_date_end_of_day.strftime('%Y-%m-%d %H:%M:%S'))

        if "audit_cycle" in filters:
            filter_conditions.append("audit_cycle = %s")
            filter_values.append(filters["audit_cycle"])

        if "department" in filters:
            filter_conditions.append("department = %s")
            filter_values.append(filters["department"])

    if filter_conditions:
        base_query += " AND " + " AND ".join(filter_conditions)

    data = frappe.db.sql(base_query, filter_values, as_dict=1)

    return columns, data


def get_columns():
    columns = [
        {
            "label": _("<b>ID</b>"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Observation Correction"
        },
        {
            "label": _("<b>Internal Audit Conformity</b>"),
            "fieldname": "internal_audit_conformity",
            "fieldtype": "Link",
            "options": "Internal Audit Conformity"
        },
        {
            "label": _("<b>Internal Audit Plan</b>"),
            "fieldname": "internal_audit_plan",
            "fieldtype": "Link",
            "options": "Internal Audit Details"
        },
        {
            "label": _("<b>Audit Cycle</b>"),
            "fieldname": "audit_cycle",
            "fieldtype": "Link",
            "options": "Audit Cycle"
        },
        {
            "label": _("<b>Department</b>"),
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department"
        },
        {
            "label": _("<b>Type</b>"),
            "fieldname": "type",
            "fieldtype": "Data"
        },
        {
            "label": _("<b>Date</b>"),
            "fieldname": "date",
            "fieldtype": "Date"
        },
        {
            "label": _("<b>Auditor</b>"),
            "fieldname": "auditor_name",
            "fieldtype": "Data"
        },
        {
            "label": _("<b>Auditee HOD</b>"),
            "fieldname": "auditee_hod_name",
            "fieldtype": "Data"
        },
        {
            "label": _("<b>Observation Detail</b>"),
            "fieldname": "observation_detail",
            "fieldtype": "Text"
        },
        {
            "label": _("<b>Correction Plan</b>"),
            "fieldname": "correction_plan",
            "fieldtype": "Text"
        },
        {
            "label": _("<b>Responsible Person</b>"),
            "fieldname": "responsible_person_name",
            "fieldtype": "Data"
        },
        {
            "label": _("<b>Planned Date of Completion</b>"),
            "fieldname": "planned_date_of_completion",
            "fieldtype": "Date"
        },
        {
            "label": _("<b>Actual Date of Completion</b>"),
            "fieldname": "actual_date_of_completion",
            "fieldtype": "Date"
        },
        {
            "label": _("<b>Reason for Delay</b>"),
            "fieldname": "reason_for_delay",
            "fieldtype": "Text"
        },
        {
            "label": _("<b>Observation Correction Status</b>"),
            "fieldname": "workflow_state",
            "fieldtype": "Data"
        },
        {"label": _("<b>Remarks</b>"), "fieldname": "remark",
         "fieldtype": "Text", "width": 200},
    ]

    return columns

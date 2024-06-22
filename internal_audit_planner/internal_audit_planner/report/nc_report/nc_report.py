# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta


def execute(filters=None):
    columns = get_columns()

    base_query = """
        SELECT
            noc.*,
            auditor_emp.full_name AS auditor_name,
            auditee_emp.full_name AS auditee_hod_name
        FROM
            `tabNon Conformity` AS noc
        LEFT JOIN
            `tabCompany Employee` AS auditor_emp ON noc.auditor = auditor_emp.name
        LEFT JOIN
            `tabCompany Employee` AS auditee_emp ON noc.auditee_hod = auditee_emp.name
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
            filter_conditions.append("noc.date BETWEEN %s AND %s")
            filter_values.append(filters["from_date"])
            filter_values.append(filters["to_date"])
        elif "from_date" in filters:
            filter_conditions.append("noc.date >= %s")
            filter_values.append(filters["from_date"])
        elif "to_date" in filters:
            to_date_end_of_day = datetime.strptime(filters["to_date"], '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
            filter_conditions.append("noc.date <= %s")
            filter_values.append(to_date_end_of_day.strftime('%Y-%m-%d %H:%M:%S'))

        if "audit_cycle" in filters:
            filter_conditions.append("audit_cycle = %s")
            filter_values.append(filters["audit_cycle"])

        if "department" in filters:
            filter_conditions.append("department = %s")
            filter_values.append(filters["department"])

        if "audit_cycle" in filters:
            filter_conditions.append("audit_cycle = %s")
            filter_values.append(filters["audit_cycle"])

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
            "options": "Non Conformity"
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
            "fieldtype": "Date"},
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
            "label": _("<b>ISO Standard</b>"),
            "fieldname": "iso_standard",
            "fieldtype": "Link",
            "options": "ISO Standard"
        },
        {
            "label": _("<b>Clause</b>"),
            "fieldname": "clause",
            "fieldtype": "Data"
        },
        {
            "label": _("<b>Non Conformity Detail</b>"),
            "fieldname": "non_conformity_detail",
            "fieldtype": "Text",
        },
        {
            "label": _("<b>Clause Reference</b>"),
            "fieldname": "clause_reference",
            "fieldtype": "Text",
        },
        {
            "label": _("<b>NC Statement</b>"),
            "fieldname": "nc_statement",
            "fieldtype": "Text"},
        {
            "label": _("<b>Objective Evidence</b>"),
            "fieldname": "objective_evidence",
            "fieldtype": "Text",
        },
        {
            "label": _("<b>Correction</b>"),
            "fieldname": "correction",
            "fieldtype": "Text"},
        {
            "label": _("<b>Root Cause of NC</b>"),
            "fieldname": "root_cause_of_nc",
            "fieldtype": "Text",
        },
        {
            "label": _("<b>CA Taken Date</b>"),
            "fieldname": "ca_taken_date",
            "fieldtype": "Date"
        },
        {
            "label": _("<b>Corrective Action Taken</b>"),
            "fieldname": "corrective_action_taken",
            "fieldtype": "Text",
        },
        {
            "label": _("<b>VECA Date</b>"),
            "fieldname": "veca_date",
            "fieldtype": "Date"
        },
        {
            "label": _("<b>Verification of Effectiveness of Corrective Action</b>"),
            "fieldname": "verification_of_effectiveness_of_corrective_action",
            "fieldtype": "Text",
        },
    ]

    return columns

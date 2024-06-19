# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()

    data = frappe.db.sql(
        """
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
    """,
        as_dict=1,
    )

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
        {"label": _("<b>Date</b>"), "fieldname": "date", "fieldtype": "Date"},
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
        {"label": _("<b>NC Statement</b>"), "fieldname": "nc_statement", "fieldtype": "Text"},
        {
            "label": _("<b>Objective Evidence</b>"),
            "fieldname": "objective_evidence",
            "fieldtype": "Text",
        },
        {"label": _("<b>Correction</b>"), "fieldname": "correction", "fieldtype": "Text"},
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

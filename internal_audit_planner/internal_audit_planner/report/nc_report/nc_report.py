# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()

    data = frappe.db.sql(
        """
    SELECT
        noc.name,
        noc.audit_date,
        noc.department,
        noc.internal_audit_number,
        auditor_emp.full_name AS auditor_name,
        auditor_emp.sign AS auditor_designation,
        auditee_emp.full_name AS auditee_name,
        auditee_emp.sign AS auditee_designation,
        noc.iso_standard,
        noc.clause,
        noc.non_conformity_detail,
        noc.clause_reference,
        noc.nc_statement,
        noc.objective_evidence,
        noc.correction,
        noc.root_cause_of_nc,
        noc.corrective_action_taken,
        noc.verification_of_effectiveness_of_corrective_action,
        noc.ca_taken_date,
        noc.veca_date
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
            "label": "Non Conformity Number",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Non Conformity"
        },
        {
            "label": "Audit Date",
            "fieldname": "audit_date",
            "fieldtype": "Date"
        },
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department"
        },
        {
            "label": "Internal Audit",
            "fieldname": "internal_audit_number",
            "fieldtype": "Link",
            "options": "Internal Audit Details"
        },
        {
            "label": "Auditor Name",
            "fieldname": "auditor_name",
            "fieldtype": "Data"
        },
        {
            "label": "Auditor Designation",
            "fieldname": "auditor_designation",
            "fieldtype": "Data"
        },
        {
            "label": "Auditee Name",
            "fieldname": "auditee_name",
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "label": "Auditee Designation",
            "fieldname": "auditee_designation",
            "fieldtype": "Data"
        },
        {
            "label": "ISO Standard",
            "fieldname": "iso_standard",
            "fieldtype": "Link",
            "options": "ISO Standard"
        },
        {
            "label": "Clause",
            "fieldname": "clause",
            "fieldtype": "Data"
        },
        {
            "label": "Non Conformity Detail",
            "fieldname": "non_conformity_detail",
            "fieldtype": "Text",
        },
        {
            "label": "Clause Reference",
            "fieldname": "clause_reference",
            "fieldtype": "Text",
        },
        {"label": "NC Statement", "fieldname": "nc_statement", "fieldtype": "Text"},
        {
            "label": "Objective Evidence",
            "fieldname": "objective_evidence",
            "fieldtype": "Text",
        },
        {"label": "Correction", "fieldname": "correction", "fieldtype": "Text"},
        {
            "label": "Root Cause of NC",
            "fieldname": "root_cause_of_nc",
            "fieldtype": "Text",
        },
        {
            "label": "CA Taken Date",
            "fieldname": "ca_taken_date",
            "fieldtype": "Date"
        },
        {
            "label": "Corrective Action Taken",
            "fieldname": "corrective_action_taken",
            "fieldtype": "Text",
        },
        {
            "label": "VECA Date",
            "fieldname": "veca_date",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "label": "Verification of Effectiveness of Corrective Action",
            "fieldname": "verification_of_effectiveness_of_corrective_action",
            "fieldtype": "Text",
        },
    ]

    return columns

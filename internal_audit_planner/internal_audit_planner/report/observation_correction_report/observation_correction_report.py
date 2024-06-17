# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()

    data = frappe.db.sql(
        """
    SELECT
        obs.name,
        obs.department,
        obs.date,
        auditor_emp.full_name AS auditor_name,
        obs.observation_details,
        auditee_hod_emp.full_name AS auditee_hod_name,
        obs.correction_plan,
        responsible_emp.full_name AS responsible_person_name,
        obs.planned_date_of_completion,
        obs.actual_date_of_completion,
        obs.reason_for_delay,
        obs.workflow_state,
        obs.remark
    FROM
        `tabObservations Corrections` AS obs
    LEFT JOIN
        `tabCompany Employee` AS auditor_emp ON obs.auditor = auditor_emp.name
    LEFT JOIN
        `tabCompany Employee` AS auditee_hod_emp ON obs.auditee_hod = auditee_hod_emp.name
    LEFT JOIN
        `tabCompany Employee` AS responsible_emp ON obs.responsible_person = responsible_emp.name
    """,
        as_dict=1,
    )
    
    print(data)

    return columns, data


def get_columns():
    columns = [
        {
            "label": "Observation",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Observations Corrections",
            "width": 150,
        },
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department",
            "width": 120,
        },
        {"label": "Date", "fieldname": "date", "fieldtype": "Date", "width": 120},
        {
            "label": "Auditor Name",
            "fieldname": "auditor_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Observation Detail",
            "fieldname": "observation_details",
            "fieldtype": "Text",
            "width": 200,
        },
        {
            "label": "Auditee HOD Name",
            "fieldname": "auditee_hod_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Correction Plan",
            "fieldname": "correction_plan",
            "fieldtype": "Text",
            "width": 200,
        },
        {
            "label": "Responsible Person",
            "fieldname": "responsible_person_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Planned Date of Completion",
            "fieldname": "planned_date_of_completion",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "label": "Actual Date of Completion",
            "fieldname": "actual_date_of_completion",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "label": "Reason for Delay",
            "fieldname": "reason_for_delay",
            "fieldtype": "Text",
            "width": 200,
        },
        {
            "label": "Observation Correction Status",
            "fieldname": "workflow_state",
            "fieldtype": "Data",
            "width": 150,
        },
        {"label": "Remarks", "fieldname": "remark", "fieldtype": "Text", "width": 200},
    ]

    return columns

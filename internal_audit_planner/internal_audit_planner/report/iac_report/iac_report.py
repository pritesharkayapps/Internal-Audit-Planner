# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta


def execute(filters=None):
    columns = get_columns()

    if not filters:
        filters = {}
        
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    conformity_filters = {}

    if filters.get('internal_audit_plan'):
        conformity_filters["internal_audit_plan"] = filters.get('internal_audit_plan')

    if from_date and to_date:
        conformity_filters["date"] = ["between", [from_date, to_date]]
    elif from_date:
        conformity_filters["date"] = [">=", from_date]
    elif to_date:
        to_date_end_of_day = datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
        conformity_filters["date"] = ["<=", to_date_end_of_day.strftime('%Y-%m-%d %H:%M:%S')]
    
    if filters.get('audit_cycle'):
        conformity_filters["audit_cycle"] = filters.get('audit_cycle')

    if filters.get('department'):
        conformity_filters["department"] = filters.get('department')
        
    data = get_data(conformity_filters)
    return columns, data


def get_columns():
    columns = [
        {
            "label": _("<b>ID</b>"),
            "fieldname": "id",
            "fieldtype": "Link",
            "options": "Internal Audit Conformity",
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
            "label": _("<b>Auditee HOD</b>"),
            "fieldname": "auditee_hod_name",
            "fieldtype": "Data"
        },
        {
            "label": _("<b>Auditor</b>"),
            "fieldname": "auditor_name",
            "fieldtype": "Data"
        },
        {
            "label": _("<b>Auditor Sign</b>"),
            "fieldname": "auditor_sign",
            "fieldtype": "Data"
        },
        {
            "label": _("<b>Reference Type</b>"),
            "fieldname": "reference_type",
            "fieldtype": "Data",
        },
        {
            "label": _("<b>Reference Title</b>"),
            "fieldname": "reference_title",
            "fieldtype": "Data",
        },
        {
            "label": _("<b>Details</b>"), "fieldname": "details", "fieldtype": "Text"},
        {
            "label": _("<b>Type</b>"), "fieldname": "type", "fieldtype": "Data"},
        {
            "label": _("<b>Reference Doc Name</b>"),
            "fieldname": "reference_doc_name",
            "fieldtype": "Data",
        },
        {
            "label": _("<b>Reference Doc Link</b>"),
            "fieldname": "reference_doc_link",
            "fieldtype": "Dynamic Link",
            "options": "reference_doc_name",
        },
    ]
    return columns


def get_data(filters):
    data = []

    conformity_records = frappe.get_all(
        "Internal Audit Conformity",
        filters=filters,
        fields=["*"],
    )

    for parent in conformity_records:
        iac_details = frappe.get_all(
            "IAC Details",
            filters={"parent": parent.name},
            fields="*"
        )

        auditee_hod_name = frappe.get_value(
            "Company Employee", parent.auditee_hod, "full_name")
        auditor_name, sign = frappe.get_value(
            "Company Employee", parent.auditor, ["full_name", "sign"])

        for idx, child in enumerate(iac_details):
            if idx == 0:
                data.append(
                    {
                        "id": parent.name,
                        "internal_audit_plan": parent.internal_audit_plan,
                        "audit_cycle": parent.audit_cycle,
                        "department": parent.department,
                        "auditee_hod_name": auditee_hod_name,
                        "auditor_name": auditor_name,
                        "auditor_sign": sign,
                        "reference_type": child.reference_type,
                        "reference_title": child.reference_title,
                        "details": child.details,
                        "type": child.type,
                        "reference_doc_name": child.reference_doc_name,
                        "reference_doc_link": child.reference_doc_link
                    }
                )
            else:
                data.append(
                    {
                        "reference_type": child.reference_type,
                        "reference_title": child.reference_title,
                        "details": child.details,
                        "type": child.type,
                        "reference_doc_name": child.reference_doc_name,
                        "reference_doc_link": child.reference_doc_link,
                    }
                )

    return data

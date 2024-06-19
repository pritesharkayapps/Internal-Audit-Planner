# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()

    data = get_data()
    return columns, data


def get_columns():
    columns = [
        {
            "label": _("<b>Internal Audit Plan</b>"),
            "fieldname": "internal_audit_plan",
            "fieldtype": "Link",
            "options": "Internal Audit Details",
        },
        {
            "label": _("<b>Department</b>"),
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department",
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
        {"label": _("<b>Details</b>"), "fieldname": "details", "fieldtype": "Text"},
        {"label": _("<b>Type</b>"), "fieldname": "type", "fieldtype": "Data", "width": 100},
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
        {
            "label": _("<b>ID</b>"),
            "fieldname": "id",
            "fieldtype": "Link",
            "options": "Internal Audit Conformity",
        },
    ]
    return columns


def get_data(filters=None):
    data = []

    conformity_records = frappe.get_all(
        "Internal Audit Conformity", fields=["*"], filters=filters
    )

    for parent in conformity_records:
        iac_details = frappe.get_all(
            "IAC Details",
            fields=[
                "reference_type",
                "reference_title",
                "details",
                "type",
                "reference_doc_name",
                "reference_doc_link",
            ],
            filters={"parent": parent.name},
        )

        for idx, child in enumerate(iac_details):
            if idx == 0:
                data.append(
                    {
                        "internal_audit_plan": parent.internal_audit_plan,
                        "department": parent.department,
                        "reference_type": child.reference_type,
                        "reference_title": child.reference_title,
                        "details": child.details,
                        "type": child.type,
                        "reference_doc_name": child.reference_doc_name,
                        "reference_doc_link": child.reference_doc_link,
                        "id": parent.name,
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

# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()

    data = get_data()
    return columns, data


def get_columns():
    columns = [
        {
            "label": "Internal Audit Number",
            "fieldname": "internal_audit_number",
            "fieldtype": "Link",
            "options": "Internal Audit Details",
        },
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department",
        },
        {
            "label": "Reference Title",
            "fieldname": "reference_title",
            "fieldtype": "Data",
        },
        {"label": "Details", "fieldname": "details", "fieldtype": "Text"},
        {"label": "Type", "fieldname": "type", "fieldtype": "Data", "width": 100},
        {
            "label": "Reference Doc Name",
            "fieldname": "reference_doc_name",
            "fieldtype": "Data",
        },
        {
            "label": "Reference Doc Link",
            "fieldname": "reference_doc_link",
            "fieldtype": "Dynamic Link",
            "options": "reference_doc_name",
        },
    ]
    return columns


def get_data(filters=None):
    data = []

    conformity_records = frappe.get_all(
        "Internal Audit Conformity", fields=["*"], filters=filters
    )

    for parent in conformity_records:
        internal_audit_number = parent.get("internal_audit_number")
        department = parent.get("department")

        iac_details = frappe.get_all(
            "IAC Details",
            fields=[
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
                        "internal_audit_number": internal_audit_number,
                        "department": department,
                        "reference_title": child.reference_title,
                        "details": child.details,
                        "type": child.type,
                        "reference_doc_name": child.reference_doc_name,
                        "reference_doc_link": child.reference_doc_link,
                    }
                )
            else:
                data.append(
                    {
                        "internal_audit_number": "",
                        "department": "",
                        "reference_title": child.reference_title,
                        "details": child.details,
                        "type": child.type,
                        "reference_doc_name": child.reference_doc_name,
                        "reference_doc_link": child.reference_doc_link,
                    }
                )

    return data

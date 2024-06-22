# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class NonConformity(Document):
    def before_submit(doc):
        if doc.workflow_state == "CA Taken":
            mandatory_fields = ['iso_standard', 'clause']

            missing_fields = [
                field for field in mandatory_fields if not doc.get(field)]

            if missing_fields:
                field_names = ', '.join(missing_fields)
                frappe.throw(
                    f"The following fields are mandatory before submitting the document: {field_names}")

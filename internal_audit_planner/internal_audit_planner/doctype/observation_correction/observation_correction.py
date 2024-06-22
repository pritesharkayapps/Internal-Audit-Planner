# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class ObservationCorrection(Document):
    def before_submit(doc):
        if doc.workflow_state == "Correction Planned":
            mandatory_fields = ['correction_plan',
                                'responsible_person', 'planned_date_of_completion']

            missing_fields = [
                field for field in mandatory_fields if not doc.get(field)]

            if missing_fields:
                field_names = ', '.join(missing_fields)
                frappe.throw(
                    f"The following fields are mandatory before submitting the document: {field_names}")

    def before_update_after_submit(doc):
        if doc.workflow_state == "Corrected":
            if not doc.actual_date_of_completion:
                frappe.throw("Actual Date of Completion field is mandatory on Corrected Status")

            if doc.planned_date_of_completion < doc.actual_date_of_completion and not doc.reason_for_delay:
                frappe.throw(
                    "Reason for delay is mandatory if the planned date of completion is less than the actual date of completion.")
                


def update_status_to_not_corrected():
    print("update_status_to_not_corrected")
    today = datetime.now()

    observations = frappe.get_all('Observation Correction', filters={
        'planned_date_of_completion': ['>', today], 'docstatus': 1, 'workflow_state': ['!=', 'corrected']})

    for observation in observations:
        doc = frappe.get_doc('Observation Correction', observation['name'])
        doc.workflow_state = "Not Corrected"
        doc.save()

    frappe.db.commit()

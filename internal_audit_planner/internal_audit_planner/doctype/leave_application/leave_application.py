# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LeaveApplication(Document):
    def before_submit(doc):
        doc.validate_schedule()

        schedule_logs = frappe.get_list(
            "Employee Schedule Log",
            filters={"link_doctype": doc.doctype, "link_name": doc.name},
        )

        for log in schedule_logs:
            schedule_log = frappe.get_doc("Employee Schedule Log", log.name)
            schedule_log.save()

    def validate_schedule(doc):
        schedule_log = frappe.get_list(
            "Employee Schedule Log",
            filters={
                "employee": doc.employee,
                "start_date": (">=", doc.start_date + " 00:00:00"),
                "end_date": ("<=", doc.end_date + " 23:59:59"),
            },
            fields=["*"],
        )

        if schedule_log:
            if schedule_log[0].link_doctype == "Leave Application":
                frappe.throw("This Employee will be on leave on this date")
            else:
                frappe.throw(
                    "This Employee will have another Audit Plan Schedule at that time"
                )

        schedule_log = frappe.new_doc("Employee Schedule Log")
        schedule_log.employee = doc.employee
        schedule_log.start_date = doc.start_date + " 00:00:00"
        schedule_log.end_date = doc.end_date + " 23:59:59"
        schedule_log.link_doctype = doc.doctype
        schedule_log.link_name = doc.name
        schedule_log.type = "Leave"
        schedule_log.save()

    def before_cancel(doc):
        schedule_logs = frappe.get_list(
            "Employee Schedule Log",
            filters={"link_doctype": doc.doctype, "link_name": doc.name},
        )

        for log in schedule_logs:
            schedule_log = frappe.get_doc("Employee Schedule Log", log.name)
            schedule_log.delete()
# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InternalAuditDetails(Document):
    def before_save(doc):
        department = frappe.get_doc("Department", doc.get("department"))

        if not department:
            frappe.throw("Department not found")

        if not department.team_leader:
            frappe.throw(
                "This Department does not have any Team Leader. Please Set Team Leader first"
            )

        has_team_leader = False
        for planned_auditee in doc.get("planned_auditee"):
            if planned_auditee.employee == department.team_leader:
                has_team_leader = True
                break

        if has_team_leader == False:
            frappe.throw("A planned audit must have a team leader")

        errors = []
        for i, row in enumerate(doc.planned_auditee, 1):
            totalLog = frappe.db.count(
                "Employee Schedule Log",
                filters={
                    "employee": row.employee,
                    "start_date": (">=", doc.audit_plan_start_date),
                    "end_date": ("<=", doc.audit_plan_end_date),
                },
            )

            if totalLog > 0:
                errors.append(
                    f"Planned Audit Employee {i} already has another schedule"
                )

        for i, row in enumerate(doc.planned_auditors, 1):
            totalLog = frappe.db.count(
                "Employee Schedule Log",
                filters={
                    "employee": row.employee,
                    "start_date": (">=", doc.audit_plan_start_date),
                    "end_date": ("<=", doc.audit_plan_end_date),
                },
            )

            if totalLog > 0:
                errors.append(
                    f"Planned Auditor Employee {i} already has another schedule"
                )

        print("error length is ",len(errors))
        for i, error in enumerate(errors, 1):
            print(error)

            frappe.msgprint(error)

    def before_submit(doc):
        doc.before_save()
        frappe.throw("xvjiuh")

        frappe.throw("xvjiuh")

        for planned_auditee in doc.get("planned_auditee"):
            schedule_log = frappe.new_doc("Employee Schedule Log")
            schedule_log.employee = planned_auditee.employee
            schedule_log.start_date = doc.audit_plan_start_date
            schedule_log.end_date = doc.audit_plan_end_date
            schedule_log.link_doctype = doc.doctype
            schedule_log.link_name = doc.name
            schedule_log.save()

        for planned_auditor in doc.get("planned_auditors"):
            schedule_log = frappe.new_doc("Employee Schedule Log")
            schedule_log.employee = planned_auditor.employee
            schedule_log.start_date = doc.audit_plan_start_date
            schedule_log.end_date = doc.audit_plan_end_date
            schedule_log.link_doctype = doc.doctype
            schedule_log.link_name = doc.name
            schedule_log.save()

        frappe.db.commit()

    def before_cancel(doc):
        schedule_logs = frappe.get_list(
            "Employee Schedule Log",
            filters={"link_doctype": doc.doctype, "link_name": doc.name},
        )

        for log in schedule_logs:
            frappe.delete_doc("Employee Schedule Log", log.name)

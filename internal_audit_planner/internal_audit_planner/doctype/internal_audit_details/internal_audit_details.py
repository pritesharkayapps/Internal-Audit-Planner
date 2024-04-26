# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InternalAuditDetails(Document):
    def before_save(doc):
        doc.validate_team_leader()
        doc.validate_plan_auditee()
        doc.validate_plan_auditor()

    def before_submit(doc):
        doc.validate_team_leader()
        doc.validate_plan_auditee()
        doc.validate_plan_auditor()

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

    def validate_plan_auditor(doc):
        team_leader_count = 0

        flag = False
        for row in doc.planned_auditors:
            if row.team_leader:
                flag = True

                team_leader_count += 1
                if team_leader_count > 1:
                    frappe.throw("Only one team leader is allowed.")
                    return
            
        if flag == False:
            frappe.throw("Add atleast one Auditor Team Leader")
            return
                
        for i, row in enumerate(doc.planned_auditee, 1):
            schedule_log = frappe.get_list(
                "Employee Schedule Log",
                filters={
                    "employee": row.employee,
                    "start_date": ("<=", doc.audit_plan_start_date),
                    "end_date": (">=", doc.audit_plan_end_date),
                },
                fields=["*"],
            )

            if schedule_log:
                if schedule_log[0].link_doctype == "Leave Application":
                    frappe.throw(f"Auditee {doc.full_name} at Row {i} will be on leave on this date")
                    return
                else:
                    frappe.throw(f"Auditee {doc.full_name} at Row {i}  will have another Audit Plan Schedule at that time")
                    return

    def validate_plan_auditee(doc):
        for i, row in enumerate(doc.planned_auditee, 1):
            schedule_log = frappe.get_list(
                "Employee Schedule Log",
                filters={
                    "employee": row.employee,
                    "start_date": ("<=", doc.audit_plan_start_date),
                    "end_date": (">=", doc.audit_plan_end_date),
                },
                fields=["*"],
            )

            if schedule_log:
                if schedule_log[0].link_doctype == "Leave Application":
                    frappe.throw(f"Auditee {doc.full_name} at Row {i} will be on leave on this date")
                    return
                else:
                    frappe.throw(f"Auditee {doc.full_name} at Row {i}  will have another Audit Plan Schedule at that time")
                    return

    def validate_team_leader(doc):
        department = frappe.get_doc("Department", doc.get("department"))

        if not department:
            frappe.throw("Department not found")
            return

        if not department.team_leader:
            frappe.throw("This Department does not have HOD")
            return

        has_hod = False
        for planned_auditee in doc.get("planned_auditee"):
            if planned_auditee.employee == department.team_leader:
                has_hod = True
                break

        if has_hod == False:
            frappe.throw("A planned audit must have a team leader")
            return
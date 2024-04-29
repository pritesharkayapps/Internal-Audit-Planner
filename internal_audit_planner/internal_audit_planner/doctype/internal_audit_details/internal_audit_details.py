# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InternalAuditDetails(Document):
    def before_save(doc):
        doc.validate_team_leader()
        doc.validate_plan_auditee()
        doc.validate_plan_auditor()
        doc.validate_employee_not_in_both()

        doc.planned_auditees_log_change()
        doc.planned_auditors_log_change()

    def validate_plan_auditor(doc):
        team_leader_count = 0

        flag = False
        for row in doc.planned_auditors:
            if row.is_auditor_team_lead:
                flag = True

                team_leader_count += 1
                if team_leader_count > 1:
                    frappe.throw("Only one team leader is allowed.")
                    return

        if flag == False:
            frappe.throw("Add atleast one Auditor Team Leader")
            return

        for i, row in enumerate(doc.planned_auditees, 1):
            schedule_log = frappe.get_list(
                "Employee Schedule Log",
                filters={
                    "employee": row.employee,
                    "start_date": ("<=", doc.audit_plan_start_date),
                    "end_date": (">=", doc.audit_plan_end_date),
                    "link_doctype": ("!=", doc.doctype),
                    "link_name": ("!=", doc.doctype),
                    "child_doctype": ("!=", "Planned Auditors"),
                },
                fields=["*"],
            )

            if schedule_log:
                if schedule_log[0].link_doctype == "Leave Application":
                    frappe.throw(
                        f"Auditee {row.employee} at Row {i} will be on leave on this date"
                    )
                    return
                else:
                    frappe.throw(
                        f"Auditee {row.employee} at Row {i} will have another Audit Plan Schedule at that time"
                    )
                    return

    def validate_plan_auditee(doc):
        for i, row in enumerate(doc.planned_auditees, 1):
            schedule_log = frappe.get_list(
                "Employee Schedule Log",
                filters={
                    "employee": row.employee,
                    "start_date": ("<=", doc.audit_plan_start_date),
                    "end_date": (">=", doc.audit_plan_end_date),
                    "link_doctype": ("!=", doc.doctype),
                    "link_name": ("!=", doc.doctype),
                    "child_doctype": ("!=", "Planned Auditees"),
                },
                fields=["*"],
            )

            if schedule_log:
                if schedule_log[0].link_doctype == "Leave Application":
                    frappe.throw(
                        f"Auditee {row.employee} at Row {i} will be on leave on this date"
                    )
                    return
                else:
                    frappe.throw(
                        f"Auditee {row.employee} at Row {i} will have another Audit Plan Schedule at that time"
                    )
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
        for planned_auditee in doc.get("planned_auditees"):
            if planned_auditee.employee == department.team_leader:
                has_hod = True
                break

        if has_hod == False:
            frappe.throw("A planned audit must have a team leader")
            return

    def validate_employee_not_in_both(doc):
        planned_auditees = doc.planned_auditees
        planned_auditors = doc.planned_auditors

        employees_in_table1 = [row.employee for row in planned_auditees]
        employees_in_table2 = [row.employee for row in planned_auditors]

        common_employees = set(employees_in_table1) & set(employees_in_table2)
        if common_employees:
            frappe.throw(
                (
                    "Employee(s) {} exists in both Planned Auditee and Planned Auditors"
                ).format(", ".join(common_employees))
            )

    def planned_auditees_log_change(doc):
        previous_planned_employee = frappe.get_all(
            "Employee Schedule Log",
            filters={
                "link_doctype": doc.doctype,
                "link_name": doc.name,
                "child_doctype": "Planned Auditees",
            },
            fields=["employee"],
        )

        previous_planned_employee = set(
            (item.employee for item in previous_planned_employee)
        )
        current_planned_employee = set((item.employee for item in doc.planned_auditees))

        match_planned_auditees = previous_planned_employee.intersection(
            current_planned_employee
        )

        planned_auditees_to_remove = previous_planned_employee.difference(
            current_planned_employee
        )
        planned_auditees_to_add = current_planned_employee.difference(
            previous_planned_employee
        )

        for planned_auditee in match_planned_auditees:
            list = frappe.get_list(
                "Employee Schedule Log",
                filters={
                    "employee": planned_auditee,
                    "link_doctype": doc.doctype,
                    "link_name": doc.name,
                    "child_doctype": "Planned Auditees",
                },
                fields=["name"],
                limit=1
            )

            schedule_log = frappe.get_doc("Employee Schedule Log", list[0].name)
            schedule_log.start_date = doc.audit_plan_start_date
            schedule_log.end_date = doc.audit_plan_end_date
            schedule_log.save()

        for planned_auditee in planned_auditees_to_add:
            schedule_log = frappe.new_doc("Employee Schedule Log")
            schedule_log.employee = planned_auditee
            schedule_log.start_date = doc.audit_plan_start_date
            schedule_log.end_date = doc.audit_plan_end_date
            schedule_log.link_doctype = doc.doctype
            schedule_log.link_name = doc.name
            schedule_log.child_doctype = ("Planned Auditees",)
            schedule_log.save()

        logs_to_delete = frappe.get_list(
            "Employee Schedule Log",
            filters={
                "employee": ["in", planned_auditees_to_remove],
                "link_doctype": doc.doctype,
                "link_name": doc.name,
                "child_doctype": "Planned Auditees",
            },
        )

        for log in logs_to_delete:
            frappe.delete_doc("Employee Schedule Log", log.name)

    def planned_auditors_log_change(doc):
        previous_planned_employee = frappe.get_all(
            "Employee Schedule Log",
            filters={
                "link_doctype": doc.doctype,
                "link_name": doc.name,
                "child_doctype": "Planned Auditors",
            },
            fields=["employee"],
        )

        previous_planned_employee = set(
            (item.employee for item in previous_planned_employee)
        )
        current_planned_employee = set((item.employee for item in doc.planned_auditors))

        match_planned_auditors = previous_planned_employee.intersection(
            current_planned_employee
        )

        planned_auditees_to_remove = previous_planned_employee.difference(
            current_planned_employee
        )
        planned_auditees_to_add = current_planned_employee.difference(
            previous_planned_employee
        )

        for planned_auditor in match_planned_auditors:
            list = frappe.get_list(
                "Employee Schedule Log",
                filters={
                    "employee": planned_auditor,
                    "link_doctype": doc.doctype,
                    "link_name": doc.name,
                    "child_doctype": "Planned Auditors",
                },
                fields=["name"],
                limit=1
            )

            schedule_log = frappe.get_doc("Employee Schedule Log", list[0].name)
            schedule_log.start_date = doc.audit_plan_start_date
            schedule_log.end_date = doc.audit_plan_end_date
            schedule_log.save()

        for planned_auditor in planned_auditees_to_add:
            schedule_log = frappe.new_doc("Employee Schedule Log")
            schedule_log.employee = planned_auditor
            schedule_log.start_date = doc.audit_plan_start_date
            schedule_log.end_date = doc.audit_plan_end_date
            schedule_log.link_doctype = doc.doctype
            schedule_log.link_name = doc.name
            schedule_log.child_doctype = "Planned Auditors"
            schedule_log.save()

        logs_to_delete = frappe.get_list(
            "Employee Schedule Log",
            filters={
                "employee": ["in", planned_auditees_to_remove],
                "link_doctype": doc.doctype,
                "link_name": doc.name,
                "child_doctype": "Planned Auditors",
            },
        )

        for log in logs_to_delete:
            frappe.delete_doc("Employee Schedule Log", log.name)

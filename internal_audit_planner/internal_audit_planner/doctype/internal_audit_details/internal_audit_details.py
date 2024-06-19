# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class InternalAuditDetails(Document):
    def validate(doc):
        if doc.status == "Planned":
            validate_hod(doc)
            validate_unique_employee(doc)
            check_for_conflicts(doc)

    def before_save(doc):
        if doc.status == "Planned":
            for row in doc.planned_auditees:
                if row.auditee_team_leader:
                    doc.planned_auditee_hod = row.employee
                    break

            for row in doc.planned_auditors:
                if row.auditor_team_leader:
                    doc.planned_auditor_team_leader = row.employee
                    break

            if not doc.planned_auditee_hod:
                frappe.throw("Auditee HOD is Required")

            if not doc.planned_auditor_team_leader:
                frappe.throw("Auditor Team Leader is Required")

    def on_update(doc):
        if doc.status == "Planned" and doc.docstatus == 0:
            update_or_create_planned_log_entry(doc)

    def before_update_after_submit(doc):
        if doc.status == "Completed" and doc.workflow_state == "Audited":
            for row in doc.actual_auditees:
                if row.auditee_team_leader:
                    doc.actual_auditee_hod = row.employee
                    break

            for row in doc.actual_auditors:
                if row.auditor_team_leader:
                    doc.actual_auditor_team_leader = row.employee
                    break

            validate_actual_hod(doc)
            validate_actual_data(doc)
            validate_actual_employee_conflicts(doc)

            update_or_create_actual_log_entry(doc)

    def before_cancel(doc):
        sql_query = """
            DELETE FROM `tabEmployee Schedule Log`
            WHERE reference_name = %s AND reference_link = %s
        """

        frappe.db.sql(sql_query, (doc.doctype, doc.name))


def validate_hod(doc):
    auditee_hods = [d for d in doc.planned_auditees if d.auditee_team_leader]
    auditor_hods = [d for d in doc.planned_auditors if d.auditor_team_leader]

    if len(auditee_hods) != 1:
        frappe.throw(_("There must be exactly one HOD in Planned Auditees."))

    if len(auditor_hods) != 1:
        frappe.throw(_("There must be exactly one HOD in Planned Auditors."))


def validate_unique_employee(doc):
    auditee_employees = {d.employee for d in doc.planned_auditees}
    auditor_employees = {d.employee for d in doc.planned_auditors}

    common_employees = auditee_employees.intersection(auditor_employees)

    if common_employees:
        frappe.throw(_("Employees cannot be in both Planned Auditees and Planned Auditors: {0}").format(
            ", ".join(common_employees)))


def check_for_conflicts(self):
    start_datetime = frappe.utils.get_datetime(self.audit_plan_start_date)
    end_datetime = frappe.utils.get_datetime(self.audit_plan_end_date)

    planned_employees = set()

    for auditee in self.get('planned_auditees'):
        planned_employees.add(auditee.employee)

    for auditor in self.get('planned_auditors'):
        planned_employees.add(auditor.employee)

    conflict_details = []
    for employee in planned_employees:
        conflicting_logs = frappe.get_all(
            'Employee Schedule Log',
            filters={
                'start_date': ['<', end_datetime],
                'end_date': ['>', start_datetime],
                'employee': employee,
                'reference_name': ['!=', self.doctype],
                'reference_link': ['!=', self.name]
            },
            fields=['name', 'employee', 'start_date', 'end_date']
        )

        if conflicting_logs:
            for log in conflicting_logs:
                conflict_details.append(
                    f"Employee {log['employee']} has a conflict from {log['start_date']} to {log['end_date']} (Record: {log['name']})"
                )

    if conflict_details:
        frappe.throw(_("Conflicting schedules found:\n{0}").format(
            "\n".join(conflict_details)))


def update_or_create_planned_log_entry(doc):
    start_datetime = frappe.utils.get_datetime(doc.audit_plan_start_date)
    end_datetime = frappe.utils.get_datetime(doc.audit_plan_end_date)

    existing_auditees_employees = frappe.get_all(
        "Employee Schedule Log",
        filters={
            "reference_name": doc.doctype,
            "reference_link": doc.name,
            "child_doctype": doc.meta.get_field("planned_auditees").options,
        },
        pluck='employee'
    )

    current_auditees_employees = set(
        (item.employee for item in doc.planned_auditees))
    
    for row in doc.planned_auditees:
        if row.employee in existing_auditees_employees:
            existing_log_name = frappe.db.get_value('Employee Schedule Log', {
                'employee': row.employee,
                'reference_name': doc.doctype,
                'reference_link': doc.name
            }, 'name')

            schedule_log = frappe.get_doc(
                'Employee Schedule Log', existing_log_name)
            schedule_log.start_date = start_datetime
            schedule_log.end_date = end_datetime
            schedule_log.save()
        else:
            frappe.get_doc({
                'doctype': 'Employee Schedule Log',
                'employee': row.employee,
                'start_date': start_datetime,
                'end_date': end_datetime,
                'reference_name': doc.doctype,
                'reference_link': doc.name,
                'type': 'Planned',
                'child_doctype': doc.meta.get_field("planned_auditees").options
            }).insert()

    for employee in existing_auditees_employees:
        if employee not in current_auditees_employees:
            existing_log_name = frappe.db.get_value('Employee Schedule Log', {
                'employee': employee,
                'reference_name': doc.doctype,
                'reference_link': doc.name
            }, 'name')

            frappe.delete_doc('Employee Schedule Log', existing_log_name)

    existing_auditors_employees = frappe.get_all(
        "Employee Schedule Log",
        filters={
            "reference_name": doc.doctype,
            "reference_link": doc.name,
            "child_doctype": doc.meta.get_field("planned_auditors").options,
        },
        pluck='employee'
    )

    current_auditors_employees = set(
        (item.employee for item in doc.planned_auditors))
    
    for row in doc.planned_auditors:
        if row.employee in existing_auditors_employees:
            existing_log_name = frappe.db.get_value('Employee Schedule Log', {
                'employee': row.employee,
                'reference_name': doc.doctype,
                'reference_link': doc.name
            }, 'name')

            schedule_log = frappe.get_doc(
                'Employee Schedule Log', existing_log_name)
            schedule_log.start_date = start_datetime
            schedule_log.end_date = end_datetime
            schedule_log.save()
        else:
            frappe.get_doc({
                'doctype': 'Employee Schedule Log',
                'employee': row.employee,
                'start_date': start_datetime,
                'end_date': end_datetime,
                'reference_name': doc.doctype,
                'reference_link': doc.name,
                'type': 'Planned',
                'child_doctype': doc.meta.get_field("planned_auditors").options
            }).insert()

    for employee in existing_auditors_employees:
        if employee not in current_auditors_employees:
            existing_log_name = frappe.db.get_value('Employee Schedule Log', {
                'employee': employee,
                'reference_name': doc.doctype,
                'reference_link': doc.name
            }, 'name')

            frappe.delete_doc('Employee Schedule Log', existing_log_name)


def validate_actual_hod(doc):
    auditee_hods = [d for d in doc.actual_auditees if d.auditee_team_leader]
    auditor_hods = [d for d in doc.actual_auditors if d.auditor_team_leader]

    if len(auditee_hods) != 1:
        frappe.throw(_("There must be exactly one HOD in Actual Auditees."))

    if len(auditor_hods) != 1:
        frappe.throw(_("There must be exactly one HOD in Actual Auditors."))


def validate_actual_employee_conflicts(doc):
    start_datetime = frappe.utils.get_datetime(doc.audit_start_date)
    end_datetime = frappe.utils.get_datetime(doc.audit_end_date)

    for i, auditee in enumerate(doc.actual_auditees, 1):
        conflicting_logs = frappe.get_all(
            'Employee Schedule Log',
            filters={
                'start_date': ['<', end_datetime],
                'end_date': ['>', start_datetime],
                'employee': auditee.employee,
                'reference_name': ['!=', doc.doctype],
                'reference_link': ['!=', doc.name]
            },
            fields=['*']
        )

        if conflicting_logs:
            if conflicting_logs[0].reference_name == "Leave Application":
                frappe.throw(
                    f"Auditee {auditee.employee} at Row {i} will be on leave on this date"
                )
                return
            else:
                frappe.throw(
                    f"Auditee {auditee.employee} at Row {i} will have another Audit Plan Schedule at that time"
                )
                return

    for i, auditee in enumerate(doc.actual_auditors, 1):
        conflicting_logs = frappe.get_all(
            'Employee Schedule Log',
            filters={
                'start_date': ['<', end_datetime],
                'end_date': ['>', start_datetime],
                'employee': auditee.employee,
                'reference_name': ['!=', doc.doctype],
                'reference_link': ['!=', doc.name]
            },
            fields=['*']
        )

        if conflicting_logs:
            if conflicting_logs[0].reference_name == "Leave Application":
                frappe.throw(
                    f"Auditee {auditee.employee} at Row {i} will be on leave on this date"
                )
                return
            else:
                frappe.throw(
                    f"Auditee {auditee.employee} at Row {i} will have another Audit Plan Schedule at that time"
                )
                return



def validate_actual_data(doc):
    auditee_employees = {d.employee for d in doc.actual_auditees}
    auditor_employees = {d.employee for d in doc.actual_auditors}

    common_employees = auditee_employees.intersection(auditor_employees)

    if common_employees:
        frappe.throw(_("Employees cannot be in both Planned Auditees and Planned Auditors: {0}").format(
            ", ".join(common_employees)))


def update_or_create_actual_log_entry(doc):
    start_datetime = frappe.utils.get_datetime(doc.audit_plan_start_date)
    end_datetime = frappe.utils.get_datetime(doc.audit_plan_end_date)

    existing_auditees_employees = frappe.get_all(
        "Employee Schedule Log",
        filters={
            "reference_name": doc.doctype,
            "reference_link": doc.name,
            "child_doctype": doc.meta.get_field("actual_auditees").options,
        },
        pluck='employee'
    )

    current_auditees_employees = set(
        (item.employee for item in doc.actual_auditees))

    for row in doc.planned_auditees:
        if row.employee in existing_auditees_employees:
            existing_log_name = frappe.db.get_value('Employee Schedule Log', {
                'employee': row.employee,
                'reference_name': doc.doctype,
                'reference_link': doc.name
            }, 'name')

            schedule_log = frappe.get_doc(
                'Employee Schedule Log', existing_log_name)
            schedule_log.start_date = start_datetime
            schedule_log.end_date = end_datetime
            schedule_log.save()
        else:
            frappe.get_doc({
                'doctype': 'Employee Schedule Log',
                'employee': row.employee,
                'start_date': start_datetime,
                'end_date': end_datetime,
                'reference_name': doc.doctype,
                'reference_link': doc.name,
                'type': 'Actual',
                'child_doctype': doc.meta.get_field("actual_auditees").options
            }).insert()

    for employee in existing_auditees_employees:
        if employee not in current_auditees_employees:
            existing_log_name = frappe.db.get_value('Employee Schedule Log', {
                'employee': employee,
                'reference_name': doc.doctype,
                'reference_link': doc.name
            }, 'name')

            frappe.delete_doc('Employee Schedule Log', existing_log_name)

    existing_auditors_employees = frappe.get_all(
        "Employee Schedule Log",
        filters={
            "reference_name": doc.doctype,
            "reference_link": doc.name,
            "child_doctype": doc.meta.get_field("actual_auditors").options,
        },
        pluck='employee'
    )

    current_auditors_employees = set(
        (item.employee for item in doc.actual_auditors))

    for row in doc.planned_auditors:
        if row.employee in existing_auditors_employees:
            existing_log_name = frappe.db.get_value('Employee Schedule Log', {
                'employee': row.employee,
                'reference_name': doc.doctype,
                'reference_link': doc.name
            }, 'name')

            schedule_log = frappe.get_doc(
                'Employee Schedule Log', existing_log_name)
            schedule_log.start_date = start_datetime
            schedule_log.end_date = end_datetime
            schedule_log.save()
        else:
            frappe.get_doc({
                'doctype': 'Employee Schedule Log',
                'employee': row.employee,
                'start_date': start_datetime,
                'end_date': end_datetime,
                'reference_name': doc.doctype,
                'reference_link': doc.name,
                'type': 'Actual',
                'child_doctype': doc.meta.get_field("actual_auditors").options
            }).insert()

    for employee in existing_auditors_employees:
        if employee not in current_auditors_employees:
            existing_log_name = frappe.db.get_value('Employee Schedule Log', {
                'employee': employee,
                'reference_name': doc.doctype,
                'reference_link': doc.name
            }, 'name')

            frappe.delete_doc('Employee Schedule Log', existing_log_name)


def send_mail(doc):
    doc_department = frappe.get_doc("Department", doc.department)
    auditees = [auditee.employee for auditee in doc.planned_auditees]
    auditors = [auditor.employee for auditor in doc.planned_auditors]

    employees = auditees+auditors

    emails = frappe.get_all("Company Employee", filters={
                            "email": ["!=", ""], "name": ["In", employees]}, pluck="email")

    recipients = emails
    sender = "pritesharkayapps@gmail.com"
    subject = f"Notification of Scheduled {doc_department.department} Audit Plan"
    message = """
    <p>I am writing to inform you that the audit plan for {department_name} has been scheduled for {audit_date} at {audit_time}. It is crucial that representatives from your department are present during this audit to provide necessary information and address any queries that may arise.</p>

    <p>Here are the details of the scheduled audit:</p>

    <ul>
        <li><strong>Audit Date:</strong> {audit_date}</li>
        <li><strong>Audit Time:</strong> {audit_time}</li>
        <li><strong>Location:</strong> {audit_location}</li>
    </ul>

    <p>Your cooperation and participation in this audit are essential to ensure its effectiveness and efficiency. Please make the necessary arrangements to have key personnel available during the audit period.</p>

    <p>If you have any questions or require further information regarding the audit process, feel free to reach out to me at {your_contact_information}.</p>

    <p>Thank you in advance for your cooperation. We look forward to your active involvement in the audit process.</p>

    <p>Best regards,</p>
    <p>
        <strong>{your_name}</strong><br>
        {your_organization}
    </p>
    """

    audit_date = frappe.utils.formatdate(
        doc.audit_plan_start_date, "dd-MM-YYYY")
    start_time = frappe.utils.format_time(doc.audit_plan_start_date, "HH:mm")
    end_time = frappe.utils.format_time(doc.audit_plan_end_date, "HH:mm")
    planned_time = f"{start_time} to {end_time}"

    formatted_html = message.format(
        department_name=doc_department.department,
        audit_date=audit_date,
        audit_time=planned_time,
        audit_location="Bhuj",
        your_contact_information="pritesharkayapps@gmail.com",
        your_name="Pritesh Kerai",
        your_organization="Arkay Apps Pvt Ltd",
    )

    frappe.sendmail(
        recipients=recipients, sender=sender, subject=subject, message=formatted_html
    )

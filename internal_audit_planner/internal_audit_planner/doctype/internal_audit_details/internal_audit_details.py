# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InternalAuditDetails(Document):
    def validate(doc):
        if doc.status == "Planned":
            validate_planned_auditees(doc)
            validate_planned_auditors(doc)
            validate_planned_data(doc)

    def before_save(doc):
        if doc.status == "Planned":
            planned_auditees_log_change(doc)
            planned_auditors_log_change(doc)

    def before_submit(doc):
        if doc.status == "Planned":
            send_mail(doc)
        
        pass

    def before_update_after_submit(doc):
        if doc.status == "Completed" and doc.workflow_state == "Audit":
            validate_actual_auditees(doc)
            validate_actual_auditors(doc)
            validate_actual_data(doc)

            actual_auditees_log_change(doc)
            actual_auditors_log_change(doc)

    def before_cancel(doc):
        sql_query = """
            DELETE FROM `tabEmployee Schedule Log`
            WHERE link_doctype = %s AND link_name = %s
        """

        frappe.db.sql(sql_query, (doc.doctype, doc.name))


def validate_planned_auditees(doc):
    hod_count = 0

    flag = False
    for row in doc.planned_auditees:
        if row.auditee_team_leader:
            flag = True
            hod_count += 1

    if hod_count > 1:
        frappe.throw("Only one HOD is allowed.")
        return

    if flag == False:
        frappe.throw("Add atleast one HOD")
        return

    for i, row in enumerate(doc.planned_auditees, 1):
        schedule_log = frappe.get_list(
            "Employee Schedule Log",
            filters={
                "employee": row.employee,
                "start_date": ("<=", doc.audit_plan_start_date),
                "end_date": (">=", doc.audit_plan_end_date),
            },
            or_filters={
                "link_doctype": ("!=", doc.doctype),
                "link_name": ("!=", doc.name),
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


def validate_planned_auditors(doc):
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

    for i, row in enumerate(doc.planned_auditors, 1):
        schedule_log = frappe.get_list(
            "Employee Schedule Log",
            filters={
                "employee": row.employee,
                "start_date": ("<=", doc.audit_plan_start_date),
                "end_date": (">=", doc.audit_plan_end_date),
            },
            or_filters={
                "link_doctype": ("!=", doc.doctype),
                "link_name": ("!=", doc.name),
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


def validate_planned_data(doc):
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


def validate_actual_auditees(doc):
    hod_count = 0

    flag = False
    for row in doc.actual_auditees:
        if row.auditee_team_leader:
            flag = True
            hod_count += 1

    if hod_count > 1:
        frappe.throw("Only one HOD is allowed.")
        return

    if flag == False:
        frappe.throw("Add atleast one HOD")
        return

    for i, row in enumerate(doc.actual_auditees, 1):
        schedule_log = frappe.get_list(
            "Employee Schedule Log",
            filters={
                "employee": row.employee,
                "start_date": ("<=", doc.audit_plan_start_date),
                "end_date": (">=", doc.audit_plan_end_date),
            },
            or_filters={
                "link_doctype": ("!=", doc.doctype),
                "link_name": ("!=", doc.name),
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


def validate_actual_auditors(doc):
    team_leader_count = 0

    flag = False
    for row in doc.actual_auditors:
        if row.is_auditor_team_lead:
            flag = True
            team_leader_count += 1

    if team_leader_count > 1:
        frappe.throw("Only one team leader is allowed.")
        return

    if flag == False:
        frappe.throw("Add atleast one Auditor Team Leader")
        return

    for i, row in enumerate(doc.actual_auditors, 1):
        schedule_log = frappe.get_list(
            "Employee Schedule Log",
            filters={
                "employee": row.employee,
                "start_date": ("<=", doc.audit_plan_start_date),
                "end_date": (">=", doc.audit_plan_end_date),
            },
            or_filters={
                "link_doctype": ("!=", doc.doctype),
                "link_name": ("!=", doc.name),
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


def validate_actual_data(doc):
    actual_auditees = doc.actual_auditees
    actual_auditors = doc.actual_auditors

    employees_in_table1 = [row.employee for row in actual_auditees]
    employees_in_table2 = [row.employee for row in actual_auditors]

    common_employees = set(employees_in_table1) & set(employees_in_table2)
    if common_employees:
        frappe.throw(
            (
                "Employee(s) {} exists in both Planned Auditee and Planned Auditors"
            ).format(", ".join(common_employees))
        )


def planned_auditees_log_change(doc):
    previous_auditees = frappe.get_all(
        "Employee Schedule Log",
        filters={
            "link_doctype": doc.doctype,
            "link_name": doc.name,
            "child_doctype": doc.meta.get_field("planned_auditees").options,
        },
        fields=["employee"],
    )

    previous_auditees = set((item.employee for item in previous_auditees))
    current_auditees = set((item.employee for item in doc.planned_auditees))

    match_auditees = previous_auditees.intersection(current_auditees)
    auditees_to_remove = previous_auditees.difference(current_auditees)
    auditees_to_add = current_auditees.difference(previous_auditees)

    for auditee in match_auditees:
        list = frappe.get_list(
            "Employee Schedule Log",
            filters={
                "employee": auditee,
                "link_doctype": doc.doctype,
                "link_name": doc.name,
                "child_doctype": doc.meta.get_field("planned_auditees").options,
            },
            fields=["name"],
            limit=1,
        )

        log = frappe.get_doc("Employee Schedule Log", list[0].name)
        log.start_date = doc.audit_plan_start_date
        log.end_date = doc.audit_plan_end_date
        log.save()

    for auditee in auditees_to_add:
        log = frappe.new_doc("Employee Schedule Log")
        log.employee = auditee
        log.start_date = doc.audit_plan_start_date
        log.end_date = doc.audit_plan_end_date
        log.link_doctype = doc.doctype
        log.link_name = doc.name
        log.child_doctype = doc.meta.get_field("planned_auditees").options
        log.type = "Planned"
        log.save()

    delete_log_list = frappe.get_list(
        "Employee Schedule Log",
        filters={
            "employee": ["in", auditees_to_remove],
            "link_doctype": doc.doctype,
            "link_name": doc.name,
            "child_doctype": doc.meta.get_field("planned_auditees").options,
        },
    )

    for log in delete_log_list:
        frappe.delete_doc("Employee Schedule Log", log.name)


def planned_auditors_log_change(doc):
    previous_auditors = frappe.get_all(
        "Employee Schedule Log",
        filters={
            "link_doctype": doc.doctype,
            "link_name": doc.name,
            "child_doctype": doc.meta.get_field("planned_auditors").options,
        },
        fields=["employee"],
    )

    previous_auditors = set((item.employee for item in previous_auditors))
    current_auditors = set((item.employee for item in doc.planned_auditors))

    match_auditors = previous_auditors.intersection(current_auditors)
    auditors_to_remove = previous_auditors.difference(current_auditors)
    auditors_to_add = current_auditors.difference(previous_auditors)

    for auditor in match_auditors:
        list = frappe.get_list(
            "Employee Schedule Log",
            filters={
                "employee": auditor,
                "link_doctype": doc.doctype,
                "link_name": doc.name,
                "child_doctype": doc.meta.get_field("planned_auditors").options,
            },
            fields=["name"],
            limit=1,
        )

        log = frappe.get_doc("Employee Schedule Log", list[0].name)
        log.start_date = doc.audit_plan_start_date
        log.end_date = doc.audit_plan_end_date
        log.save()

    for auditor in auditors_to_add:
        log = frappe.new_doc("Employee Schedule Log")
        log.employee = auditor
        log.start_date = doc.audit_plan_start_date
        log.end_date = doc.audit_plan_end_date
        log.link_doctype = doc.doctype
        log.link_name = doc.name
        log.child_doctype = doc.meta.get_field("planned_auditors").options
        log.type = "Planned"
        log.save()

    delete_log_list = frappe.get_list(
        "Employee Schedule Log",
        filters={
            "employee": ["in", auditors_to_remove],
            "link_doctype": doc.doctype,
            "link_name": doc.name,
            "child_doctype": doc.meta.get_field("planned_auditors").options,
        },
    )

    for log in delete_log_list:
        frappe.delete_doc("Employee Schedule Log", log.name)


def actual_auditees_log_change(doc):
    previous_auditees = frappe.get_all(
        "Employee Schedule Log",
        filters={
            "link_doctype": doc.doctype,
            "link_name": doc.name,
            "child_doctype": doc.meta.get_field("actual_auditees").options,
        },
        fields=["employee"],
    )

    previous_auditees = set((item.employee for item in previous_auditees))
    current_auditees = set((item.employee for item in doc.actual_auditees))

    match_auditees = previous_auditees.intersection(current_auditees)
    auditees_to_remove = previous_auditees.difference(current_auditees)
    auditees_to_add = current_auditees.difference(previous_auditees)

    for auditee in match_auditees:
        list = frappe.get_list(
            "Employee Schedule Log",
            filters={
                "employee": auditee,
                "link_doctype": doc.doctype,
                "link_name": doc.name,
                "child_doctype": doc.meta.get_field("actual_auditees").options,
            },
            fields=["name"],
            limit=1,
        )

        log = frappe.get_doc("Employee Schedule Log", list[0].name)
        log.start_date = doc.audit_start_date
        log.end_date = doc.audit_end_date
        log.save()

    for auditee in auditees_to_add:
        log = frappe.new_doc("Employee Schedule Log")
        log.employee = auditee
        log.start_date = doc.audit_start_date
        log.end_date = doc.audit_end_date
        log.link_doctype = doc.doctype
        log.link_name = doc.name
        log.child_doctype = doc.meta.get_field("actual_auditees").options
        log.type = "Actual"
        log.save()

    delete_log_list = frappe.get_list(
        "Employee Schedule Log",
        filters={
            "employee": ["in", auditees_to_remove],
            "link_doctype": doc.doctype,
            "link_name": doc.name,
            "child_doctype": doc.meta.get_field("actual_auditees").options,
        },
    )

    for log in delete_log_list:
        frappe.delete_doc("Employee Schedule Log", log.name)


def actual_auditors_log_change(doc):
    previous_auditors = frappe.get_all(
        "Employee Schedule Log",
        filters={
            "link_doctype": doc.doctype,
            "link_name": doc.name,
            "child_doctype": doc.meta.get_field("actual_auditors").options,
        },
        fields=["employee"],
    )

    previous_auditors = set((item.employee for item in previous_auditors))
    current_auditors = set((item.employee for item in doc.actual_auditors))

    match_auditors = previous_auditors.intersection(current_auditors)
    auditors_to_remove = previous_auditors.difference(current_auditors)
    auditors_to_add = current_auditors.difference(previous_auditors)

    for auditor in match_auditors:
        list = frappe.get_list(
            "Employee Schedule Log",
            filters={
                "employee": auditor,
                "link_doctype": doc.doctype,
                "link_name": doc.name,
                "child_doctype": doc.meta.get_field("actual_auditors").options,
            },
            fields=["name"],
            limit=1,
        )

        log = frappe.get_doc("Employee Schedule Log", list[0].name)
        log.start_date = doc.audit_start_date
        log.end_date = doc.audit_end_date
        log.save()

    for auditor in auditors_to_add:
        log = frappe.new_doc("Employee Schedule Log")
        log.employee = auditor
        log.start_date = doc.audit_start_date
        log.end_date = doc.audit_end_date
        log.link_doctype = doc.doctype
        log.link_name = doc.name
        log.child_doctype = doc.meta.get_field("actual_auditors").options
        log.type = "Actual"
        log.save()

    delete_log_list = frappe.get_list(
        "Employee Schedule Log",
        filters={
            "employee": ["in", auditors_to_remove],
            "link_doctype": doc.doctype,
            "link_name": doc.name,
            "child_doctype": doc.meta.get_field("actual_auditors").options,
        },
    )

    for log in delete_log_list:
        frappe.delete_doc("Employee Schedule Log", log.name)


def send_mail(doc):
    doc_department = frappe.get_doc("Department",doc.department)
    auditees = [auditee.employee for auditee in doc.planned_auditees]
    auditors = [auditor.employee for auditor in doc.planned_auditors]

    employees = auditees+auditors

    emails = frappe.get_all("Company Employee", filters={"email": ["!=", ""],"name":["In",employees]}, pluck="email")

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

    audit_date = frappe.utils.formatdate(doc.audit_plan_start_date, "dd-MM-YYYY")
    start_time = frappe.utils.format_time(doc.audit_plan_start_date,"HH:mm")
    end_time = frappe.utils.format_time(doc.audit_plan_end_date,"HH:mm")
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

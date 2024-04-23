# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InternalAuditDetails(Document):
	def before_save(doc):
		department = frappe.get_doc("Department", doc.get('department'))

		if not department:
			return "Department not Found"
		pass

	def before_submit(doc):
		for planned_auditee in doc.get('planned_auditee'):
			schedule_log = frappe.new_doc("Employee Schedule Log")
			schedule_log.employee = planned_auditee.employee
			schedule_log.start_date = doc.audit_plan_start_date
			schedule_log.end_date = doc.audit_plan_end_date
			schedule_log.save()

		for planned_auditor in doc.get('planned_auditors'):
			schedule_log = frappe.new_doc("Employee Schedule Log")
			schedule_log.employee = planned_auditor.employee
			schedule_log.start_date = doc.audit_plan_start_date
			schedule_log.end_date = doc.audit_plan_end_date
			schedule_log.save()

		frappe.db.commit()


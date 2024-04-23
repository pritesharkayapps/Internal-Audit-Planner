# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LeaveApplication(Document):
	def before_submit(doc):
		schedule_log = frappe.new_doc("Employee Schedule Log")
		schedule_log.employee = doc.employee
		schedule_log.start_date = doc.start_date + " 00:00:00"
		schedule_log.end_date = doc.end_date + " 23:59:59"
		schedule_log.save()

		frappe.db.commit()

# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EmployeeScheduleLog(Document):
    pass


@frappe.whitelist()
def check_employee_schedules(employee=None, start_date=None, end_date=None):
	doc = frappe.get_doc("Company Employee", employee)

	if not doc:
		return "Employee not Found"

	totalEmployeeScheduleLog = frappe.db.count(
		"Employee Schedule Log",
		filters={
			"employee": employee,
			"start_date": ("<=", start_date),
			"end_date": (">=", end_date),
		}
	)

	if totalEmployeeScheduleLog > 0:
		return f"{doc.full_name} already has another schedule on this date"

	return
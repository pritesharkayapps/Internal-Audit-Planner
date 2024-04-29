# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Department(Document):
	def before_save(doc):
		if doc.team_leader:
			employee = frappe.get_doc("Company Employee",doc.team_leader)

			employee.team_leader = 1
			employee.save()
			
	pass

@frappe.whitelist()
def get_auditee(department):
	department_res = frappe.get_doc('Department',department)

	if not department_res:
		frappe.throw("Department not found")

	employee_list = frappe.get_list("Company Employee",filters={
		"department":department,
		"is_auditor":False
	},fields=["*"])

	return {
		"department":department_res,
		"list":employee_list
	}
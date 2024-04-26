# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json


class EmployeeScheduleLog(Document):
    pass


@frappe.whitelist()
def check_employee_schedules(employee=None, start_date=None, end_date=None):
	doc = frappe.get_doc("Company Employee", employee)

	if not doc:
		return "Employee not Found"

	schedule_log = frappe.get_list(
		"Employee Schedule Log",
		filters={
			"employee": employee,
			"start_date": ("<=", start_date),
			"end_date": (">=", end_date),
		},fields=["*"],
	)

	if schedule_log:
		if schedule_log[0].link_doctype == "Leave Application":
			frappe.throw(f"{doc.full_name} will be on leave on this date")
			return
		else:
			frappe.throw(f"{doc.full_name} will have another Audit Plan Schedule at that time")
			return

@frappe.whitelist()
def get_events(doctype, start, end, field_map, filters=None, fields=None):
	field_map = frappe._dict(json.loads(field_map))
	fields = frappe.parse_json(fields)

	doc_meta = frappe.get_meta(doctype)
	for d in doc_meta.fields:
		if d.fieldtype == "Color":
			field_map.update({"color": d.fieldname})

	filters = json.loads(filters) if filters else []

	start_date = "ifnull(%s, '0001-01-01 00:00:00')" % field_map.start
	end_date = "ifnull(%s, '2199-12-31 00:00:00')" % field_map.end

	filters += [
		[doctype, start_date, "<=", end],
		[doctype, end_date, ">=", start],
	]
	events = frappe.get_list(doctype, fields=["*"], filters=filters)

	for event in events:
		employee = frappe.get_doc("Company Employee",event.employee)
		if event.link_doctype == "Leave Application":
			event.color = "#F08080"
			event.subject = f"{employee.full_name} is On Leave"
		else:
			internal_audit = frappe.get_doc("Internal Audit Details",event.link_name)

			event.color = "#6495ED"
			event.subject = f"{employee.full_name} has already Planned in {internal_audit.name}"

	return events

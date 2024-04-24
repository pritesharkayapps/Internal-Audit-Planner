frappe.views.calendar["Employee Schedule Log"] = {
	get_events_method: "internal_audit_planner.internal_audit_planner.doctype.employee_schedule_log.employee_schedule_log.get_events",
	field_map: {
		"start": "start_date",
		"end": "end_date",
		"id": "name",
		"title": "subject",
		"allDay": "allDay",
		"progress": "progress"
	}
};
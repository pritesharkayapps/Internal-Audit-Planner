frappe.views.calendar["Employee Schedule Log"] = {
	get_events_method: "internal_audit_planner.internal_audit_planner.doctype.employee_schedule_log.employee_schedule_log.get_events",
	field_map: {
		start: "start_date",
		end: "end_date",
		id: "name",
		allDay: "all_day",
		title: "subject",
		status: "event_type",
		color: "color",
	},
	style_map: {
		Public: "success",
		Private: "info",
	},
};
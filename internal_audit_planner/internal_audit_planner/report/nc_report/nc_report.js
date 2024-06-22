// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.query_reports["NC Report"] = {
	"filters": [
		{
			fieldname: 'internal_audit_conformity',
			label: __('Internal Audit Conformity'),
			fieldtype: 'Link',
			options: "Internal Audit Conformity"
		},
		{
			fieldname: 'internal_audit_plan',
			label: __('Internal Audit Plan'),
			fieldtype: 'Link',
			options: "Internal Audit Details"
		},
		{
			fieldname: 'from_date',
			label: __('From Date'),
			fieldtype: 'Date'
		},
		{
			fieldname: 'to_date',
			label: __('To Date'),
			fieldtype: 'Date'
		},
		{
			fieldname: 'audit_cycle',
			label: __('Audit Cycle'),
			fieldtype: 'Link',
			options: "Audit Cycle"
		},
		{
			fieldname: 'department',
			label: __('Department'),
			fieldtype: 'Link',
			options: "Department"
		},
		{
			fieldname: 'iso_standard',
			label: __('ISO Standard'),
			fieldtype: 'Link',
			options: "ISO Standard"
		},
	]
};

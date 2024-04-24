// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.ui.form.on("Internal Audit Details", {
    refresh(frm) {
    },
});

frappe.ui.form.on("Planned Auditees", {
    employee: async function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];

        if (row.employee) {
            frappe.call({
                method: "internal_audit_planner.internal_audit_planner.doctype.employee_schedule_log.employee_schedule_log.check_employee_schedules",
                type: "GET",
                args: {
                    'employee': row.employee,
                    'start_date': frm.doc.audit_plan_start_date,
                    'end_date': frm.doc.audit_plan_end_date
                }
            }).then((resp) => {
                if (resp.message) {
                    frappe.msgprint(resp.message)
                    frappe.model.set_value(cdt, cdn, "employee", null);
                }
            })
        }
    },
});

frappe.ui.form.on("Planned Auditors", {
    employee: async function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];

        if (row.employee) {
            frappe.call({
                method: "internal_audit_planner.internal_audit_planner.doctype.employee_schedule_log.employee_schedule_log.check_employee_schedules",
                type: "GET",
                args: {
                    'employee': row.employee,
                    'start_date': frm.doc.audit_plan_start_date,
                    'end_date': frm.doc.audit_plan_end_date
                }
            }).then((resp) => {
                if (resp.message) {
                    frappe.msgprint(resp.message)
                    frappe.model.set_value(cdt, cdn, "employee", null);
                }
            })
        }
    },
});
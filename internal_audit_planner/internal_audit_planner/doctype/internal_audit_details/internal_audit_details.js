// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.ui.form.on("Internal Audit Details", {
    refresh: function (frm) {
        var today = new Date();

        frm.fields_dict['audit_plan_start_date'].datepicker.update({
            minDate: today
        });
    },
    audit_plan_start_date: function (frm) {
        var start_date = new Date(frappe.datetime.add_days(frm.doc.audit_plan_start_date))

        frm.fields_dict['audit_plan_end_date'].datepicker.update({
            minDate: start_date
        });
    },
    department: function (frm) {
        var department = frm.doc.department

        frappe.call({
            method: "internal_audit_planner.internal_audit_planner.doctype.department.department.get_auditee",
            type: "GET",
            args: {
                'department': department,
            }
        }).then((resp) => {
            department = resp.message.department
            employees = resp.message.list

            frm.clear_table('planned_auditee');
            
            for (i = 0; i < employees.length; i++) {
                var row = frappe.model.add_child(frm.doc, 'planned_auditee');
                row.employee = employees[i].name
                
                if(department.team_leader && department.team_leader == employees[i].name) {
                    row.audit_leader = 1
                }
            }

            frm.refresh_field('planned_auditee');
        })
    }
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
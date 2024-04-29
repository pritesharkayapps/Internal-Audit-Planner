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

            frm.clear_table('planned_auditees');

            for (i = 0; i < employees.length; i++) {
                var row = frappe.model.add_child(frm.doc, 'planned_auditees');
                row.employee = employees[i].name
                if (employees[i].team_leader) {
                    row.auditee_team_leader = 1
                }

                // if (department.team_leader && department.team_leader == employees[i].name) {
                //     row.auditee_team_leader = 1
                // }
            }

            frm.refresh_field('planned_auditees');
        })
    },
    status: function (frm) {
        var status = frm.doc.status

        if (status == "Completed") {
            copyPlannedData(frm)
        }
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
                    'filters':{
                        'link_doctype':["!=",frm.doc.doctype],
                        'link_name':["!=",frm.doc.name],
                        "child_doctype": ["!=","Planned Auditees"],
                    },
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
                    'filters':{
                        'link_doctype':["!=",frm.doc.doctype],
                        'link_name':["!=",frm.doc.name],
                        "child_doctype": ["!=","Planned Auditors"],
                    },
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

function copyPlannedData(frm) {
    plan_start_date = frm.doc.audit_plan_start_date
    plan_end_date = frm.doc.audit_plan_end_date
    planned_auditees = frm.doc.planned_auditees
    planned_auditors = frm.doc.planned_auditors

    audit_start_date = frm.doc.audit_start_date
    audit_end_date = frm.doc.audit_end_date
    actual_auditees = frm.doc.actual_auditees
    actual_auditors = frm.doc.actual_auditors
    
    if (!audit_start_date && !audit_end_date && actual_auditees.length == 0 && actual_auditors.length == 0) {
        frm.set_value('audit_start_date', plan_start_date)
        frm.set_value('audit_end_date', plan_end_date)

        frm.doc.planned_auditees.forEach(function (row) {
            var newRow = frm.add_child('actual_auditees');
            newRow.employee = row.employee;
            newRow.auditee_team_leader = row.auditee_team_leader;
        });

        frm.doc.planned_auditors.forEach(function (row) {
            var newRow = frm.add_child('actual_auditors');
            newRow.employee = row.employee;
            newRow.is_auditor_team_lead = row.is_auditor_team_lead;
        });

        frm.refresh_fields(['actual_auditees', 'actual_auditors']);
    }

}
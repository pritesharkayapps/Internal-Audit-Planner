// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

totalQualifiedCourseforLeader = 0
frappe.call({
    method: "internal_audit_planner.internal_audit_planner.doctype.audit_objective.audit_objective.record_count",
    type: "GET"
}).then((resp) => {
    totalQualifiedCourseforLeader = resp.message
})

console.log(totalQualifiedCourseforLeader)

let d;

frappe.ui.form.on("Company Employee", {
    setup(frm) {
        d = new frappe.ui.Dialog({
            title: 'Qualified for Auditor Team Leader',
            fields: [
                {
                    label: 'Is Auditor Team Leader',
                    fieldname: 'is_auditor_team_leader',
                    fieldtype: 'Check'
                },
            ],
            size: 'small',
            primary_action_label: 'Submit',
            primary_action(values) {
                frm.set_value('is_auditor_team_leader', values.is_auditor_team_leader)
                d.hide();
            }
        });
    },
    refresh(frm) {
        var corsesTableLength = frm.doc.employee_courses.length || [];

        if (corsesTableLength == 0) {
            frappe.db.get_list('Audit Objective', {
                fields: ['*'],
            }).then(records => {
                for (var i = 0; i < records.length; i++) {
                    row = cur_frm.add_child("employee_courses");
                    row.course = records[i].course_name

                    refresh_field("employee_courses");
                }
            })
        }
    },
    site: function (frm) {
        site = frm.doc.site

        if (site) {
            frm.set_query('department', function () {
                return {
                    filters: [
                        ['site', '=', site]
                    ]
                };
            });
        }
    },
});


frappe.ui.form.on("Employee Courses", {
    valid_from: async function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];

        validToDate = row.valid_from;
        var validToDate = new Date(validToDate);
        validToDate.setFullYear(validToDate.getFullYear() + 3);
        frappe.model.set_value(cdt, cdn, "valid_to", validToDate);
    },
    valid_to: async function (frm, cdt, cdn) {
        CheckIsTeamMember(frm, cdt, cdn)
    },
    qualified: async function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];

        if (row.qualified == 1 && frm.doc.is_auditor == 0) {
            frm.set_value('is_auditor', 1)
        }

        if (row.qualified === 0 && frm.doc.is_auditor === 1) {
            let flag = true

            frm.doc.employee_courses.forEach(function (child) {
                if (child.qualified === 1) {
                    flag = false;
                }
            })

            if (flag === true) {
                frm.set_value('is_auditor', 0)
            }
        }

        CheckIsTeamMember(frm, cdt, cdn)
    },
});

function CheckIsTeamMember(frm, cdt, cdn) {
    var coursesRecords = frm.doc.employee_courses || [];
    var noofQualifiedCourse = 0;

    coursesRecords.forEach(function (record) {
        frappe.call({
            method: "internal_audit_planner.internal_audit_planner.doctype.audit_objective.audit_objective.record_exist",
            type: "GET",
            args: {
                filters: {
                    'course_name': record.course,
                    'mandatory_for_team_lead': 1
                }
            }
        }).then((resp) => {
            if (resp.message == 1 && record.qualified == 1) {
                noofQualifiedCourse++
            }

            console.log(totalQualifiedCourseforLeader, noofQualifiedCourse)

            if (totalQualifiedCourseforLeader == noofQualifiedCourse && frm.doc.is_auditor_team_leader == 0) {
                d.show();
            } else {
                frm.set_value('is_auditor_team_leader', 0)
            }
        })
    });
}
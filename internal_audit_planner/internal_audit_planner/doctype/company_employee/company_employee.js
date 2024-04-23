// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

totalQualifiedCourseforLeader = 0
frappe.call({
    method: "internal_audit_planner.internal_audit_planner.doctype.course.course.record_count",
    type: "GET"
}).then((resp) => {
    totalQualifiedCourseforLeader = resp.message
})

let d;

frappe.ui.form.on("Company Employee", {
    setup(frm) {
        d = new frappe.ui.Dialog({
            title: 'User is qualified for Auditor',
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
        // frm.set_df_property("is_auditor_team_leader", 'read_only', 1);

        var corsesTableLength = frm.doc.employee_courses.length || [];

        if (corsesTableLength == 0) {
            frappe.db.get_list('Course', {
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
        CheckIsTeamMember(frm, cdt, cdn)
    },
});

function CheckIsTeamMember(frm, cdt, cdn) {
    var coursesRecords = frm.doc.employee_courses || [];
    var noofQualifiedCourse = 0;

    coursesRecords.forEach(function (record) {
        if (record.valid_to >= frappe.datetime.now_date()) {
            frappe.call({
                method: "internal_audit_planner.internal_audit_planner.doctype.course.course.record_exist",
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

                if (totalQualifiedCourseforLeader == noofQualifiedCourse) {
                    d.show();
                }
            })
        }
    });
}
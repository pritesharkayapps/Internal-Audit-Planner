// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.ui.form.on("Company Employee", {
    refresh(frm) {
        frm.set_df_property("is_auditor_team_leader", 'read_only', 1);
    },
    is_auditor: function (frm) {
        if (frm.doc.is_auditor == 0) {
            frm.set_df_property("is_auditor_team_leader", 'read_only', 1);
            frm.refresh_fields();
        } else if (frm.doc.is_auditor == 1) {
            frm.set_df_property("is_auditor_team_leader", 'read_only', 0);
            frm.refresh_fields();
        }
    },
    is_auditor_team_leader: function (frm) {
        if (frm.doc.is_auditor_team_leader == 1) {
            frappe.db.get_list('Course', {
                fields: ['*'],
                filters: {
                    mandatory_for_auditor: 1
                }
            }).then(records => {
                var d = records.length > 0 ? records : []
                for (var i = 0; i < d.length; i++) {
                    row = cur_frm.add_child("employee_courses");
                    row.course = d[i].course_name
                    refresh_field("employee_courses");
                }
            })
        }
    }
});

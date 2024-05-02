// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.ui.form.on("Department", {
    refresh(frm) {
        department = frm.doc.name

        frm.set_query('team_leader', function () {
            return {
                filters: [
                    ['department', '=', department]
                ]
            };
        });
    },
});

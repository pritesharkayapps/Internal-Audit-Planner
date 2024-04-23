// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.ui.form.on("Leave Application", {
    start_date: function(frm) {
        calculateDaysDifference(frm);
    },
    end_date: function(frm) {
        calculateDaysDifference(frm);
    }
});

function calculateDaysDifference(frm) {
    var start_date = frm.doc.start_date;
    var end_date = frm.doc.end_date;
    if (start_date && end_date) {
        var days = frappe.datetime.get_diff(end_date, start_date) + 1;
        frm.set_value('leave_days', days);
    }
}
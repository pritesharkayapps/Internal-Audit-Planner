// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.ui.form.on("Leave Application", {
    refresh: function (frm) {
        if (frm.is_new()) {
            var today = new Date();

            frm.fields_dict['start_date'].datepicker.update({
                minDate: today
            });
        }
    },
    start_date: function (frm) {
        var start_date = new Date(frappe.datetime.add_days(frm.doc.start_date))

        frm.fields_dict['end_date'].datepicker.update({
            minDate: start_date
        });

        calculateDaysDifference(frm);
    },
    end_date: function (frm) {
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
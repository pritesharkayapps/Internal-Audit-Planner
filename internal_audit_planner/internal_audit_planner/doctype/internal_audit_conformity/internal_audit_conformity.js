// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.ui.form.on("Internal Audit Conformity", {
    refresh: function (frm) {
        if (!frm.is_new() && frm.doc.docstatus === 0) {
            frm.add_custom_button('Create Reports', function () {
                frappe.call({
                    method: 'internal_audit_planner.internal_audit_planner.doctype.internal_audit_conformity.internal_audit_conformity.generate_reports',
                    args: {
                        docname: frm.doc.name
                    },
                    callback: function (r) {
                        frappe.msgprint(r.message);

                        frm.reload_doc();
                    }
                });
            });
        }
    },
    onload: function (frm) {
        frm.fields_dict['iac_details'].grid.get_field('reference_doc_link').get_query = function (doc, cdt, cdn) {
            return {
                filters: {
                    'internal_audit_conformity': frm.doc.name
                }
            };
        };
    },
    internal_audit_plan: function (frm) {
        if (frm.doc.internal_audit_plan) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Internal Audit Details',
                    name: frm.doc.internal_audit_plan
                },
                callback: function (r) {
                    if (r.message) {
                        frm.clear_table('actual_auditees');

                        $.each(r.message.actual_auditees, function (index, row) {
                            var new_row = frm.add_child('actual_auditees');
                            new_row.employee = row.employee
                            new_row.auditee_team_leader = row.auditee_team_leader
                        });

                        frm.refresh_field('actual_auditees');
                        frm.clear_table('actual_auditors');

                        $.each(r.message.actual_auditors, function (index, row) {
                            var new_row = frm.add_child('actual_auditors');
                            new_row.employee = row.employee
                            new_row.auditor_team_leader = row.auditor_team_leader
                        });

                        frm.refresh_field('actual_auditors');
                    }
                }
            });
        }
    }
});

frappe.ui.form.on('IAC Details', {
    type: function (frm, cdt, cdn) {
        var child = locals[cdt][cdn];
        if (child.type) {
            if (['P', 'AFI', 'O'].includes(child.type)) {
                frappe.model.set_value(cdt, cdn, 'reference_doc_name', 'Observation Correction');

                frm.fields_dict['iac_details'].grid.fields_map['reference_doc_link'].get_route_options_for_new_doc = function (field) {
                    return {
                        "internal_audit_conformity": frm.doc.name,
                        "type": child.type
                    };
                };
            } else if (['NC', 'M'].includes(child.type)) {
                frappe.model.set_value(cdt, cdn, 'reference_doc_name', 'Non Conformity');

                frm.fields_dict['iac_details'].grid.fields_map['reference_doc_link'].get_route_options_for_new_doc = function (field) {
                    return {
                        "internal_audit_conformity": frm.doc.name,
                        "type": child.type === 'M' ? 'Major' : child.type
                    };
                };
            }
        }
    }
});
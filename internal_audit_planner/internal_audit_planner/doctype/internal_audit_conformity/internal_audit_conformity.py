# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InternalAuditConformity(Document):
    pass


@frappe.whitelist()
def generate_reports(docname):
    doc = frappe.get_doc('Internal Audit Conformity',docname)
    
    iac_details = frappe.get_all('IAC Details', filters={
        'parenttype': doc.doctype, 'parent': doc.name}, fields="*")

    for iac_detail in iac_details:
        if not iac_detail.reference_doc_link:
            if iac_detail.type == "O":
                observation = frappe.new_doc('Observation Correction')
                observation.internal_audit_conformity = doc.name
                observation.type = 'O'
                observation.observation_details = iac_detail.details
                observation.save()

                frappe.db.set_value('IAC Details', iac_detail.name,
                                    'reference_doc_name', observation.doctype)
                frappe.db.set_value(
                    'IAC Details', iac_detail.name, 'reference_doc_link', observation.name)

            elif iac_detail.type in ["NC","M"]:
                nc_type = None
                if iac_detail.type == "NC":
                    nc_type = "NC"
                elif iac_detail.type == "M":
                    nc_type = "Major"

                nc = frappe.new_doc('Non Conformity')
                nc.internal_audit_conformity = doc.name
                nc.type = nc_type
                nc.non_conformity_detail = iac_detail.details
                nc.save()

                frappe.db.set_value(
                    'IAC Details', iac_detail.name, 'reference_doc_name', nc.doctype)
                frappe.db.set_value(
                    'IAC Details', iac_detail.name, 'reference_doc_link', nc.name)
                
    return "IAC Details Reports generated Successfully."

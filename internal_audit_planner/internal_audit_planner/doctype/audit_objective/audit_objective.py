# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AuditObjective(Document):
    pass


@frappe.whitelist()
def record_exist(filters=None):
    first_record = frappe.get_list(
        "AuditObjective", filters=filters, limit_start=0, limit_page_length=1
    )

    if first_record:
        return True
    else:
        return False


@frappe.whitelist()
def record_count(filters=None):
    return frappe.db.count("AuditObjective", filters={"mandatory_for_team_lead": 1})

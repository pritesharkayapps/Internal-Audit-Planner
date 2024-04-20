# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CompanyEmployee(Document):
    def before_save(self):
        self.full_name = " ".join(
            filter(None, [self.salutation, self.first_name, self.last_name])
        )

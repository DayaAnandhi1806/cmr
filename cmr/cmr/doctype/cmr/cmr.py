# Copyright (c) 2023, Frutter Software Labs Private Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CMR(Document):
	pass

@frappe.whitelist()
def get_all_employees():
    employees = frappe.get_all("Employee", filters={"status": "Active"}, fields=["name", "employee_name"])
    return [{"value": employee.name, "label": f"{employee.name} - {employee.employee_name}"} for employee in employees]

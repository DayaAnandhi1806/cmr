// Copyright (c) 2023, Frutter Software Labs Private Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["CMR Summary Report"] = {
	"filters": [
		{
			fieldname:"date",
			label: __("Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today()
		},
		{
			fieldname: "ftd",
			label: __("FTD"),
			fieldtype: "Data",
			default: "FTD",
			read_only: 1
		},
		{
			fieldname: "mtd",
			label: __("MTD"),
			fieldtype: "Data",
			default: "MTD",
			read_only: 1
		}
	],
	"onload": function(report) {
		// Apply styles after the page has loaded
		const redFilter = report.page.fields_dict["ftd"];
		const mtdFilter = report.page.fields_dict["mtd"];

		if (redFilter) {
			redFilter.input.style.backgroundColor = "red";
			redFilter.input.style.color = "white";
			redFilter.input.style.width = "50px"; // Adjust the width as needed
			redFilter.input.style.fontWeight = "bold";
		}

		if (mtdFilter) {
			mtdFilter.input.style.backgroundColor = "green";
			mtdFilter.input.style.color = "white";
			mtdFilter.input.style.width = "55px";
			mtdFilter.input.style.fontWeight = "bold";
		}
	}
};
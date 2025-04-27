# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:14:00 2025

@author: adeda
"""

import pandas as pd
import json

# Read the Excel file with the additional column
excel_file = 'indo_vat_category.xlsx'  # Make sure this file exists in your directory
data = pd.read_excel(excel_file)

# Extract relevant columns 
products = data[['_curr_law', 'Description', 'VAT_Rate']].to_dict(orient='records')

# Create a dictionary to hold all product data
output_data = {}

# Construct each product's JSON structure
for product in products:
    product_key = product['_curr_law']
    output_data[product_key] = {
        "long_name": f"VAT Rate for {product['Description']}",
        "description": f"VAT Rate relevant for consumption of {product['Description']}",
        "itr_ref": "VAT Rules",
        "notes": "",
        "row_var": "AYEAR",
        "row_label": ["2018"],
        "start_year": 2018,
        "cpi_inflatable": False,
        "cpi_inflated": False,
        "col_var": "",
        "col_label": "",
        "boolean_value": False,
        "integer_value": False,
        "value": [product['VAT_Rate']],
        "range": {
            "min": 0,
            "max": 1
        },
        "out_of_range_minmsg": "",
        "out_of_range_maxmsg": "",
        "out_of_range_action": "stop"
    }

# Write the output data to a JSON file
with open('current_law_policy_vat_Indonesia_category1.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)

print("JSON file created successfully with extra descriptions.")

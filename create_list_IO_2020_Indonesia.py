# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 07:29:52 2025

@author: adeda
"""

import pandas as pd
import json

# Read the Excel file
excel_file = 'indo_vat_category.xlsx'
df = pd.read_excel(excel_file)
# Create the products list from the DataFrame
products = df[['Category4', 'CONS', 'Rate_name', 'vat_calc', 'Description']].to_dict(orient='records')

# Generate the second output dictionary (read)
output_calc = {
    "calc": {
        "vatax": {
            "type": "float",
            "category": "None",
            "desc": "Total vat liability",
            "form": {
                "2018": "National Household Survey 2018"
            },
        }
    }
}

for product in products:
    output_calc["calc"][product['vat_calc']] = {
        "type": "float",
        "Category": 'None',
        "desc": f"vat liability of {product['Description']}",
        "form": {
            "susenas 2018": "National Household Survey 2018"
        },
    }


with open('records_variable_indo_category.json', 'w') as json_file:
    json.dump(output_calc, json_file, indent=4)

print("output_calc.json and output_read.json have been created.")

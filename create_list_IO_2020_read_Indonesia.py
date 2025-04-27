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
output_read = {
    "read": {
        "id_n": {
            "required" : "true",
            "type": "float",
            "category": "None",
            "desc": "Unique positive numeric identifier for filing unit",
            "form": {
                "2018": "National Household Survey 2018"
            },
            "cross_year": "No",
            "attribute": "No"
            },
        "Year": {
            "required" : "true",
            "type": "float",
            "category": "None",
            "desc": "Assessment Year",
            "form": {
                "2018": "National Household Survey 2018"
            },
            "cross_year": "No",
            "attribute": "No"
        }
    }
}

for product in products:
    output_read["read"][product['CONS']] = {
        "type": "float",
        "category": "None",
        "desc": f"Household consumption of {product['Description']}",
        "form": {
            "2018": "National Household Survey 2018"
        },
        "cross_year": "No",
        "attribute": "No"
    }


with open('output_read.json', 'w') as json_file:
    json.dump(output_read, json_file, indent=4)

print("output_calc.json and output_read.json have been created.")

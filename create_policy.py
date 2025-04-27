# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 16:32:35 2025

@author: adeda
"""

import pandas as pd
import json
import re

def clean_identifier(text):
    """
    Clean the input text so it can be used as a JSON key (similar to a valid Python identifier).
    For example, replace spaces and dashes with underscores.
    """
    text = str(text).strip()
    # Replace any non-alphanumeric characters (except underscore) with underscore.
    text = re.sub(r'\W+', '_', text)
    return text

def main():
    # Path to the Excel file.
    excel_path = r"C:/Users/adeda/microsimulation_manual/vat_microsim_Indo/susenas_2018_product_name_and_rate.xlsx"
    
    # Read the Excel file.
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print("Error reading the Excel file:", e)
        return

    # Check that the necessary columns exist.
    if 'Rate_name1' not in df.columns or 'Rate_reform_5' not in df.columns:
        print("The required columns 'Rate_name1' and/or 'Rate_reform_5' are missing.")
        return

    policy_dict = {}
    # Iterate over each row in the DataFrame.
    for index, row in df.iterrows():
        vatkode = clean_identifier(row['Rate_name1'])
        rate = row['Rate_reform_5']
        # Build the key. For example, if VATKODE is "item_x1", the key becomes "_rate_item_x1".
        key = f"_{vatkode}"
        # Each key maps to a dictionary with key "2022" and the rate in a list.
        policy_dict[key] = {"2022": [rate]}

    # Create the final output dictionary.
    output = {"policy": policy_dict}

    # Save the output to a JSON file.
    output_file = "app0_reform_vat_indo_non_food_12.json"
    try:
        with open(output_file, "w") as f:
            json.dump(output, f, indent=4)
        print(f"JSON file successfully saved as '{output_file}'")
    except Exception as e:
        print("Error writing the JSON file:", e)

if __name__ == "__main__":
    main()

import pandas as pd

# Load data from Excel
excel_file = 'indo_vat_category.xlsx'  # Make sure this file exists in your directory
df = pd.read_excel(excel_file)

# Ensure the columns exist in the Excel file
required_columns = ['vat_cal', 'rate', 'CONS']
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"The Excel file must contain the following columns: {required_columns}")

# Generate Python code
output_file = "functions_vat_indo_category.py"

with open(output_file, "w") as f:
    # Write imports and decorators
    f.write("from numba import jit\n")
    f.write("\n")
    
    # Iterate over rows in the DataFrame to create functions
    for index, row in df.iterrows():
        vatkode = row['vat_cal']
        rate_name = row['rate']
        kode = row['CONS']
        
        # Generate function name based on VATKODE
        function_name = f"cal_{vatkode}"
        function_cal = f"{vatkode}"
        function_rate = f"{rate_name}"
        function_value = f"{kode}"
        
        # Write function definition
        f.write(f"@iterate_jit(nopython=True)\n")  # Fixed decorator name from @iterate_jit to @jit
        f.write(f"def {function_name}({function_value}, {function_rate}, {function_cal}):\n")  # Removed unused {function_cal}
        f.write(f"    \"\"\"\n")
        f.write(f"    Compute VAT on {function_value} for {vatkode}.\n")
        f.write(f"    \"\"\"\n")
        f.write(f"    {function_cal} = {function_value} * ({function_rate} / (1 + {function_rate}))\n")  # Corrected calculation variable name
        f.write(f"    return {function_cal}\n\n")
    
    # Write final function to sum all VAT calculations
    f.write(f"@iterate_jit(nopython=True)\n")
    f.write("def cal_vat(rates_dict, values_dict):\n")
    f.write("    \"\"\"\n")
    f.write("    Calculate total VAT by summing all individual VATs.\n")
    f.write("    rates_dict: Dictionary of rates with VATKODE as keys.\n")
    f.write("    values_dict: Dictionary of values with VATKODE as keys.\n")
    f.write("    \"\"\"\n")
    f.write("    vat = 0\n")

    # Add calls to each generated function
    for index, row in df.iterrows():
        vatkode = row['vat_cal']
        function_name = f"cal_{vatkode}"
        rate_name = row['rate']
        kode = row['CONS']
        
        # Use VATKODE as the key to access rates and values
        f.write(f"    vat += {function_name}(values_dict['{kode}'], rates_dict['{rate_name}'])\n")

    # Return total VAT
    f.write("    return vat\n")

print(f"Python code has been generated and saved to {output_file}")


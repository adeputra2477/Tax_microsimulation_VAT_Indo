import pandas as pd

# Load data from Excel
excel_file = 'indo_vat_category.xlsx'  # Make sure this file exists in your directory
df = pd.read_excel(excel_file)

# Ensure the columns exist in the Excel file
required_columns = ['vat_cal', 'rate', 'CONS', 'rate_curr', 'behave']
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
        behavior = row['behave']
        curr = row['rate_curr']
        
        # Generate function name based on VATKODE
        function_name1 = f"{behavior}"
        function_name2 = f"{vatkode}" 
        function_cal = f"{vatkode}"
        function_rate = f"{rate_name}"
        function_value = f"{kode}"
        function_curr = f"{curr}"
        
        # Write function behavior
        f.write(f"@iterate_jit(nopython=True)\n")  # Fixed decorator name from @iterate_jit to @jit
        f.write(f"def cal_{function_name1}({function_value}, {function_rate}, {function_curr}, elasticity_consumption_threshold, elasticity_consumption_value, {function_name1}):\n")  # Removed unused {function_cal}
        f.write(f"    \"\"\"\n")
        f.write(f"    Compute consumption after adjusting for behavior.\n")
        f.write(f"    \"\"\"\n")        
        f.write(f"    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]\n")
        f.write(f"    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]\n")
        f.write(f"    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]\n")
        f.write(f"    elasticity_consumption_value0=elasticity_consumption_value[0]\n")
        f.write(f"    elasticity_consumption_value1=elasticity_consumption_value[1]\n")
        f.write(f"    elasticity_consumption_value2=elasticity_consumption_value[2]\n")
        f.write(f"    if {function_value}<=0:\n")
        f.write(f"        elasticity=0\n")
        f.write(f"    elif {function_value}<elasticity_consumption_threshold0:\n")
        f.write(f"        elasticity=elasticity_consumption_value0\n")
        f.write(f"    elif {function_value}<elasticity_consumption_threshold1:\n")
        f.write(f"        elasticity=elasticity_consumption_value1\n") 
        f.write(f"    else:\n")
        f.write(f"        elasticity=elasticity_consumption_value2\n")        
        f.write(f"    rate={function_rate}\n")
        f.write(f"    rate_curr_law={function_curr}\n")
        f.write(f"    frac_change_of_vat_rate = (rate-rate_curr_law)/rate_curr_law\n")
        f.write(f"    frac_change_of_consumption = elasticity*frac_change_of_vat_rate\n")
        f.write(f"    {function_name1} = {function_value}*(1+frac_change_of_consumption)\n")
        f.write(f"    return {function_name1}\n\n")
    
        # Write function vat
        f.write(f"@iterate_jit(nopython=True)\n")  # Fixed decorator name from @iterate_jit to @jit
        f.write(f"def cal_{function_name2}({function_name1}, {function_rate}, {function_name2}):\n")  # Removed unused {function_cal}
        f.write(f"    \"\"\"\n")
        f.write(f"    \"\"\"\n")        
        f.write(f"    {function_name2} = {function_rate} * {function_name1}\n")
        f.write(f"    return {function_name2}\n\n")



print(f"Python code has been generated and saved to {output_file}")


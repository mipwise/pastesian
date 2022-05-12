from pastesian import input_schema, output_schema
from pastesian import solve
from test_pastesian.action_local_data_integrity import local_data_integrity_check, local_fix_bad_data

# Creating "dat" object, containing all input data
input_path = "data/inputs"
output_path = "data/outputs"
dat = input_schema.csv.create_pan_dat(input_path)

# Checking data integrity and fixing some possible related issues
local_data_integrity_check(dat)

# Optimize and populate the output schema's tables
sln = solve(dat)
output_schema.csv.write_directory(sln, output_path)

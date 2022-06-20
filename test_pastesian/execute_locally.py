from pastesian import input_schema, output_schema
from pastesian import solve
from test_pastesian.action_local_data_integrity import local_data_integrity_check
import os

# Creating "dat" object, containing all input data
input_path = os.path.join(os.path.dirname(__file__), "data/inputs")
dat = input_schema.csv.create_pan_dat(input_path)

# Checking data integrity
local_data_integrity_check(dat)

# Optimize
sln = solve(dat)

# Populate the output schema's tables
output_path = os.path.join(os.path.dirname(__file__), "data/outputs")
output_schema.csv.write_directory(sln, output_path)

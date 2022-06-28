from pastesian import input_schema, output_schema
from pastesian import solve
from test_pastesian.action_local_data_integrity import local_data_integrity_check
import os
import inspect


def _this_directory():
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))


# Create "dat" object, containing all input data
input_path = os.path.join(_this_directory(), "data/inputs")
dat = input_schema.csv.create_pan_dat(input_path)

# Check data integrity
local_data_integrity_check(dat)

# Optimize
sln = solve(dat)

# Populate the output schema's tables
output_path = os.path.join(_this_directory(), "data/outputs")
output_schema.csv.write_directory(sln, output_path)

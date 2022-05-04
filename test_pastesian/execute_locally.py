from pastesian import input_schema, output_schema
from pastesian import update_demand
from pastesian import solve

input_path = "data/inputs"
output_path = "data/outputs"
dat = input_schema.csv.create_pan_dat(input_path)
sln = solve(dat)
output_schema.csv.write_directory(sln, output_path)

# print(dat)
# print('Actual Demand')
# print(dat.demand)
# print('-'*30)
#
# dat = update_demand(dat)
# print('New Demand')
# print(dat.demand)

# print('-'*30)
# input_schema.csv.write_directory(dat, path)

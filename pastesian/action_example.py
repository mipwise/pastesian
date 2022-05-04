# this is just an example of input action. It updates the demand using as multiplier the production capacity parameter
from pastesian import input_schema


def update_demand(dat):
    demand = dat.demand.copy()
    multiplier = input_schema.create_full_parameters_dict(dat)['Production Capacity']
    demand['Demand'] = multiplier * demand['Demand']
    demand = demand.round({'Demand': 1})
    dat.demand = demand
    return dat

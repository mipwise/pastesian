"""
This is just an example of input action. It updates the demand using as multiplier the production capacity parameter
"""
from pastesian import input_schema


def action_update_demand(dat):
    """
    Update 'Demand' field of demand.csv table from input data (dat parameter) using as multiplier the production
    capacity parameter (as mentioned, just an example).

    Parameters
    ----------
    dat : PanDat
        A PanDat object containing the input data.

    Returns
    -------
    dat : PanDat
        A PanDat object containing the input data with updated 'Demand' field from 'demand.csv' table.
    """
    demand = dat.demand.copy()
    multiplier = input_schema.create_full_parameters_dict(dat)['Production Capacity']
    demand['Demand'] = multiplier * demand['Demand']

    # keep demand an integer number, as defined in the input_schema
    demand = demand.round({'Demand': 0})
    demand = demand.astype({'Demand': int})

    dat.demand = demand
    return dat

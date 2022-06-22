"""
This is just an example of input action. It updates the demand using as multiplier the production capacity parameter
"""
from pastesian import input_schema


def action_update_demand(dat):
    """
    Update demand from input data using as multiplier the production capacity parameter.

    Parameters
    ----------
    dat : PanDat
        A PanDat object containing the input data.

    Returns
    -------
    dat : PanDat
        A PanDat object containing the input data with updated demand.
    """

    demand = dat.demand.copy()
    multiplier = input_schema.create_full_parameters_dict(dat)['Production Capacity']
    demand['Demand'] = multiplier * demand['Demand']
    demand = demand.round({'Demand': 1})
    dat.demand = demand
    return dat

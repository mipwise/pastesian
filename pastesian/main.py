from pastesian import input_schema, output_schema
import pulp
import pandas as pd
from pastesian.utils import check_each_period_id_column


def solve(dat):
    """
    Main function of pastesian, from the input data it optimizes the system and return output tables.

    :param dat: PanDat object containing the input data.

    :return: sln: PanDat object containing the output data.
    """
    # region Prepare optimization parameters
    check_each_period_id_column(dat)  # verify that each 'Period ID' column is valid

    d = dict(zip(dat.demand['Period ID'], dat.demand['Demand']))  # dict: {period_id: demand}
    pc = dict(zip(dat.costs['Period ID'], dat.costs['Production Cost']))  # dict: {period_id: production_cost}
    ic = dict(zip(dat.costs['Period ID'], dat.costs['Inventory Cost']))  # dict: {period_id: inventory_cost}

    # Ensure 'costs' and 'demand' tables have the same 'Period ID' columns
    d_set = set(d.keys())  # creates a set from demand['Period ID']
    pc_set = set(pc.keys())  # creates a set from costs['Period ID']
    d_minus_pc = d_set.difference(pc_set)
    pc_minus_d = pc_set.difference(d_set)
    if d_minus_pc:
        raise ValueError(f'The following indexes exist in demand["Period ID"] but not in costs["Period ID"]: '
                         f'{d_minus_pc}')
    if pc_minus_d:
        raise ValueError(f'The following indexes exist in costs["Period ID"] but not in demand["Period ID"]: '
                         f'{pc_minus_d}')

    # Variables keys
    I = list(dat.demand['Period ID'])  # list like [1, 2, 3, ...] with periods' numbers, not necessarily ordered. We
    # could also have used dat.costs['Period ID'] since the above verification ensure they're the same, except possibly
    # for ordering.

    # endregion

    # region Build optimization model
    mdl = pulp.LpProblem('Pastesian', sense=pulp.LpMinimize)
    x = pulp.LpVariable.dicts(indexs=I, cat=pulp.LpContinuous, lowBound=0.0, name='x')  # Production quantities
    s = pulp.LpVariable.dicts(indexs=I, cat=pulp.LpContinuous, lowBound=0.0, name='s')  # Storage quantities

    parameters = input_schema.create_full_parameters_dict(dat)

    # region Flow Balance constraints
    for i in I:
        if i == 1:
            # In the first period, we use 'Lasagnas To Start' parameter as storage quantity from "previous" period
            starting_amount = parameters['Lasagnas To Start']
            mdl.addConstraint(x[i] + starting_amount == s[i] + d[i], name=f'balance_at_{i}')
        else:
            # In the middle periods, we have the usual flow balance constraints
            mdl.addConstraint(x[i] + s[i-1] == d[i] + s[i], name=f'balance_at_{i}')

    # In the last period, we use 'Lasagnas To Be Left' (default=0) parameter as storage quantity to be left to
    # the next horizon
    left_amount = parameters['Lasagnas To Be Left']
    mdl.addConstraint(s[max(I)] == left_amount, name=f'last_storage')
    # endregion

    # region Capacity constraints
    # TODO: think about varying capacities through periods. They should come with input data
    prod_capacity = parameters['Production Capacity']
    if prod_capacity != -1:
        for i in I:
            mdl.addConstraint(x[i] <= prod_capacity, name=f'prod_capacity_{i}')

    inv_capacity = parameters['Inventory Capacity']
    if inv_capacity != -1:
        for i in I:
            mdl.addConstraint(s[i] <= inv_capacity, name=f'inv_capacity_{i}')
    # endregion

    # region Objective function
    production_cost = pulp.lpSum(pc[i] * x[i] for i in I)
    inventory_cost = pulp.lpSum(ic[i] * s[i] for i in I)
    mdl.setObjective(production_cost + inventory_cost)
    # endregion
    # endregion

    # region Optimize and retrieve the solution
    mdl.solve()
    status = pulp.LpStatus[mdl.status]
    if status == 'Optimal':
        x_sol = [(key, var.value()) for key, var in x.items()]
        s_sol = [(key, var.value()) for key, var in s.items()]
    else:
        x_sol = None
        s_sol = None
        print(f'Model is not optimal. Status: {status}')
    # endregion

    sln = output_schema.PanDat()

    # region Populate output schema
    if x_sol:
        x_df = pd.DataFrame(x_sol, columns=['Period ID', 'Production Quantity'])
        s_df = pd.DataFrame(s_sol, columns=['Period ID', 'Inventory Quantity'])

        # Ordering the above DataFrames by increasing 'Period ID' number, more convenient for retrieving
        x_df.sort_values(axis=0, by='Period ID', inplace=True)
        s_df.sort_values(axis=0, by='Period ID', inplace=True)

        # populate production_flow table
        production_flow = x_df.merge(s_df, on='Period ID', how='right')
        production_flow.sort_values(axis=0, by='Period ID', inplace=True)  # Ordering by increasing 'Period ID', more
        # convenient for retrieving

        # production_flow = production_flow.merge(dat.time_periods[['Period ID', 'Time Period']], on='Period ID',
        #                                         how='left')
        production_flow = production_flow.astype({'Period ID': int, 'Production Quantity': 'Float64',
                                                  'Inventory Quantity': 'Float64'})
        sln.production_flow = production_flow[['Period ID', 'Production Quantity', 'Inventory Quantity']]

        # populate costs table
        prod_cost = dat.costs.merge(production_flow, on='Period ID', how='left')
        prod_cost['Production Cost'] = prod_cost['Production Quantity'] * prod_cost['Production Cost']
        prod_cost['Inventory Cost'] = prod_cost['Inventory Quantity'] * prod_cost['Inventory Cost']
        prod_cost['Total Cost'] = prod_cost['Production Cost'] + prod_cost['Inventory Cost']
        prod_cost = prod_cost.round({'Production Cost': 2, 'Inventory Cost': 2, 'Total Cost': 2})
        prod_cost = prod_cost.astype({'Period ID': int, 'Production Cost': 'Float64', 'Inventory Cost': 'Float64',
                                      'Total Cost': 'Float64'})
        prod_cost.sort_values(axis=0, by='Period ID', inplace=True)  # Ordering by increasing 'Period ID'
        sln.costs = prod_cost[['Period ID', 'Production Cost', 'Inventory Cost', 'Total Cost']]
    # endregion

    return sln

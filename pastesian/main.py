from pastesian import input_schema, output_schema
import pulp
import pandas as pd


def solve(dat):
    # Prepare optimization parameters
    I = list(dat.time_periods['Period ID'])  # list like [1, 2, 3, ...] with periods' numbers
    D = dict(zip(I, dat.demand['Demand']))  # Dictionary: {time_period: demand}
    PC = dict(zip(I, dat.costs['Production Cost']))  # Dictionary: {time_period: production_cost}
    IC = dict(zip(I, dat.costs['Inventory Cost']))  # Dictionary: {time_period: inventory_cost}

    # Build optimization model
    mdl = pulp.LpProblem('Pastesian', sense=pulp.LpMinimize)
    x = pulp.LpVariable.dicts(indexs=I, cat=pulp.LpInteger, lowBound=0.0, name='x')  # Production quantities
    s = pulp.LpVariable.dicts(indexs=I, cat=pulp.LpInteger, lowBound=0.0, name='s')  # Storage quantities

    parameters = input_schema.create_full_parameters_dict(dat)
    for i in I:
        if i == 1:
            # In the first period, we use 'Lasagnas To Start' parameter as storage quantity from "previous" period
            starting_amount = parameters['Lasagnas To Start']
            mdl.addConstraint(x[i] + starting_amount == s[i] + D[i], name=f'balance_at_{i}')
        elif i == I[-1]:
            # In the last period, we use 'Lasagnas To Be Left' (default=0) parameter as storage quantity to be left to
            # the next horizon
            left_amount = parameters['Lasagnas To Be Left']
            mdl.addConstraint(x[i] + s[i-1] == D[i] + left_amount, name=f'balance_at_{i}')
        else:
            # In the middle periods, we have the usual flow balance constraints
            mdl.addConstraint(x[i] + s[i-1] == D[i] + s[i], name=f'balance_at_{i}')

    production_cost = pulp.lpSum(PC[i] * x[i] for i in I)
    inventory_cost = pulp.lpSum(IC[i] * s[i] for i in I)
    mdl.setObjective(production_cost + inventory_cost)

    # Optimize and retrieve the solution
    mdl.solve()
    status = pulp.LpStatus[mdl.status]
    if status == 'Optimal':
        x_sol = [(key, var.value()) for key, var in x.items()]
        s_sol = [(key, var.value()) for key, var in s.items()]
    else:
        x_sol = None
        s_sol = None
        print(f'Model is not optimal. Status: {status}')

    # Populate output schema
    sln = output_schema.PanDat()
    if x_sol:
        x_df = pd.DataFrame(x_sol, columns=['Period ID', 'Production Quantity'])
        s_df = pd.DataFrame(s_sol, columns=['Period ID', 'Inventory Quantity'])
        # populate production_flow table
        production_flow = x_df.merge(s_df, on='Period ID', how='right')
        production_flow = production_flow.merge(dat.time_periods['Period ID'], on='Period ID', how='left')
        production_flow = production_flow.astype({'Period ID': int, 'Production Quantity': int,
                                                  'Inventory Quantity': int})
        sln.production_flow = production_flow[['Period ID', 'Production Quantity', 'Inventory Quantity']]
        # populate costs table
        prod_cost = x_df['Production Quantity'] * dat.costs['Production Cost']
        inv_cost = s_df['Inventory Quantity'] * dat.costs['Inventory Cost']
        sln.costs = pd.concat(dat.time_periods['Period ID'], prod_cost, inv_cost)
    return sln

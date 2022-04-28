import pulp


# slices. Syntax: "length: amount"
slices = {1: 3, 2: 2, 3: 2, 5: 2, 10: 3, 20: 3, 25: 2, 50: 1}

# sheets after being cut. Syntax: "sheet_ID: length"
sheets = {1: 22, 2: 49, 3: 3, 4: 68, 5: 71}
# sheets 1 and 2 -> 1
# sheets 3 and 4 -> 2
# sheet 5        -> 3

# Indexes for variables
I = [(i, j) for i in slices for j in sheets]

# Define the model
mdl = pulp.LpProblem('Random_puzzle', sense=pulp.LpMaximize)

# Add decision variables. x_{i,j} is the amount of i-length slices cut from the j-th sheet
x = pulp.LpVariable.dicts(indexs=I, cat=pulp.LpInteger, name='x', lowBound=0)

# Constraints

# right amount of each slice
for i in slices:
    mdl.addConstraint(sum(x[i, j] for j in sheets) == slices[i], name=f'right_amount_slice_{i}')

# no waste of material from each sheet
for j in sheets:
    mdl.addConstraint(sum(i * x[i, j] for i in slices) == sheets[j], name=f'no_waste_sheet_{j}')

# Set objective function
mdl.setObjective(x[1, 1])

# Optimize
mdl.solve()

# Retrieve the solution. Syntax: "length: amount"
cuts_sheet1 = {i: x[i, 1].value() for i in slices if x[i, 1].value() > 0.5}
cuts_sheet2 = {i: x[i, 2].value() for i in slices if x[i, 2].value() > 0.5}
cuts_sheet3 = {i: x[i, 3].value() for i in slices if x[i, 3].value() > 0.5}
cuts_sheet4 = {i: x[i, 4].value() for i in slices if x[i, 4].value() > 0.5}
cuts_sheet5 = {i: x[i, 5].value() for i in slices if x[i, 5].value() > 0.5}

print("-"*40)
print("slice length: amount")
print("Sheet 1: ", cuts_sheet1)
print("Sheet 2: ", cuts_sheet2)
print("Sheet 3: ", cuts_sheet3)
print("Sheet 4: ", cuts_sheet4)
print("Sheet 5: ", cuts_sheet5)

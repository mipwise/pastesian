import pulp


# region Input Data
# Number of darts of each one
I = {1, 2, 3, 4, 5, 6}
# Available points
J = {1, 2, 3, 5, 10, 20, 25, 50}
# Known shots (amount of shots in each point region)
S = {1: 3, 2: 2, 3: 2, 5: 2, 10: 3, 20: 3, 25: 2, 50: 1}
# People. index: [name, points, amount_darts]
people = {1: ["Andrea", 49, 4], 2: ["Andrea_son", 22, 2], 3: ["Antônio", 68, 5], 4: ["Antônio_filho", 3, 1], 5: ["Luiz", 71, 6]}
# endregion

# region Define the Model
# Define the model
mdl = pulp.LpProblem('Darts-puzzle', sense=pulp.LpMaximize)

# Decision Variables: x_{i,j} is the amount of darts person "i" threw at region "j"
keys = [(i, j) for i in people for j in S]
x = pulp.LpVariable.dicts(indexs=keys, cat=pulp.LpInteger, name='x', lowBound=0, upBound=6)

# Constraints
# Each person threw 6 darts and scored 71 points
for i in people:
    mdl.addConstraint(sum(x[i, j] for j in S) == people[i][2], name=f'person_{i}_6_darts')
    mdl.addConstraint(sum(j * x[i, j] for j in S) == people[i][1], name=f'person_{i}_71_points')

# Each region had the right amount of darts
for j in S:
    mdl.addConstraint(sum(x[i, j] for i in people) == S[j], name=f'region_{j}_amount_darts')

# Set objective
mdl.setObjective(x[1,1])

# Optimize
mdl.solve()

# Retrieve the solution

# endregion

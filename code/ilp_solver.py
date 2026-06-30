import numpy as np
import pulp

def solve_ilp(cost, distance, w, supply, demand, route_cap):

    c_mat = cost + w * distance
    W = cost.shape[0]   
    C = cost.shape[1]  

    prob = pulp.LpProblem("SmartDeliveryILP", pulp.LpMinimize)

    x = {}
    for i in range(W):
        for j in range(C):
            ub = int(route_cap[i, j])
            x[(i, j)] = pulp.LpVariable(f"x_{i}_{j}", lowBound=0, upBound=ub, cat='Integer')

    # objective
    prob += pulp.lpSum(c_mat[i, j] * x[(i, j)] for i in range(W) for j in range(C))

    # supply constraints
    for i in range(W):
        prob += pulp.lpSum(x[(i, j)] for j in range(C)) <= int(supply[i])

    # demand constraints
    for j in range(C):
        prob += pulp.lpSum(x[(i, j)] for i in range(W)) == int(demand[j])

    # solve using CBC via PuLP
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    x_val = np.zeros((W, C), dtype=int)
    for i in range(W):
        for j in range(C):
            x_val[i, j] = int(pulp.value(x[(i, j)]))

    total_cost = float(np.sum(c_mat * x_val))
    return {"x": x_val, "total_cost": total_cost, "status": pulp.LpStatus[prob.status]}

import numpy as np
import os
import time
import json
import pandas as pd

def generate_dataset(W,C,outdir="data", seed=None):
 
    os.makedirs(outdir, exist_ok=True)

    if seed is None:
        seed = int(time.time() * 1000000) % (2**32 - 1)

    np.random.seed(seed)
    
    cost = np.random.randint(3, 15, size=(W, C))
    distance = np.random.randint(5, 60, size=(W, C))
    demand = np.random.randint(50, 200, size=C)
    total_demand = demand.sum()
    supply = np.random.randint(100, 300, size=W)

    if supply.sum() < total_demand:
        supply[0] += total_demand - supply.sum()

    route_capacity = np.random.randint(100, 300, size=(W, C))

    for j in range(C):
        col_sum = route_capacity[:, j].sum()
        if col_sum < demand[j]:
            diff = demand[j] - col_sum
            route_capacity[0, j] += diff


    instance = {
        "seed": int(seed),
        "W": int(W),
        "C": int(C),
        "cost": cost.tolist(),
        "distance": distance.tolist(),
        "supply": supply.tolist(),
        "demand": demand.tolist(),
        "route_capacity": route_capacity.tolist(),
    }

    instance_path = os.path.join(outdir, "instance.json")
    with open(instance_path, "w") as f:
        json.dump(instance, f, indent=4)

    # ===== Create a human-readable table file =====
    tables_path = os.path.join(outdir, "instance_tables.txt")

    cost_df = pd.DataFrame(
        cost,
        index=[f"W{i+1}" for i in range(W)],
        columns=[f"C{j+1}" for j in range(C)],
    )
    dist_df = pd.DataFrame(
        distance,
        index=[f"W{i+1}" for i in range(W)],
        columns=[f"C{j+1}" for j in range(C)],
    )
    supply_df = pd.DataFrame(
        supply.reshape(1, -1),
        index=["Supply"],
        columns=[f"W{i+1}" for i in range(W)],
    )
    demand_df = pd.DataFrame(
        demand.reshape(1, -1),
        index=["Demand"],
        columns=[f"C{j+1}" for j in range(C)],
    )
    route_df = pd.DataFrame(
        route_capacity,
        index=[f"W{i+1}" for i in range(W)],
        columns=[f"C{j+1}" for j in range(C)],
    )

    with open(tables_path, "w") as f:
        f.write("=== Instance Overview ===\n")
        f.write(f"Seed: {seed}\n")
        f.write(f"Warehouses (W): {W}\n")
        f.write(f"Customers (C): {C}\n")
        f.write(f"Total supply: {supply.sum()}\n")
        f.write(f"Total demand: {demand.sum()}\n")
        f.write(f"Supply - Demand: {supply.sum() - demand.sum()}\n")
        f.write("=========================\n\n")

        f.write("Cost matrix (cost per unit from warehouse i to customer j):\n")
        f.write(cost_df.to_string())
        f.write("\n\n")

        f.write("Distance matrix (distance between warehouse i and customer j):\n")
        f.write(dist_df.to_string())
        f.write("\n\n")

        f.write("Supply per warehouse:\n")
        f.write(supply_df.to_string())
        f.write("\n\n")

        f.write("Demand per customer:\n")
        f.write(demand_df.to_string())
        f.write("\n\n")

        f.write("Route capacity matrix (max units on route i->j):\n")
        f.write(route_df.to_string())
        f.write("\n")

    return instance



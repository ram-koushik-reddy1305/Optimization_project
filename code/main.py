import os
import argparse
import numpy as np
import pandas as pd

from ilp_solver import solve_ilp
from utils import plot_heatmap, plot_warehouse_utilization
from generate_dataset import generate_dataset

# --- Paths ---
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT, "data")
OUTPUT_DIR = os.path.join(ROOT, "output")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    print("=== Smart Delivery Optimization ===\n")

    parser = argparse.ArgumentParser(description="Smart Delivery Optimization")
    parser.add_argument("-W", "--warehouses", type=int, help="Number of warehouses [1-15]")
    parser.add_argument("-C", "--customers", type=int, help="Number of customers [1-15]")
    parser.add_argument("-w", "--weight", type=float, help="Distance weight [0-1]")
    args = parser.parse_args()

    # Fallback to interactive prompts if arguments are not provided
    if args.warehouses is not None:
        W_arg = args.warehouses
    else:
        try:
            W_arg = int(input("Number of warehouses (W)[1-15]: "))
        except ValueError:
            print("Error: W should be an integer\n")
            return

    if W_arg < 1 or W_arg > 15:
        print("Error :W should be in the range [1-15]\n")
        return

    if args.customers is not None:
        C_arg = args.customers
    else:
        try:
            C_arg = int(input("Number of customers (C)[1-15]: "))
        except ValueError:
            print("Error: C should be an integer\n")
            return

    if C_arg < 1 or C_arg > 15:
        print("Error :C should be in the range [1-15]\n")
        return

    if args.weight is not None:
        w = args.weight
    else:
        try:
            w = float(input("Distance weight (w)[0-1]: "))
        except ValueError:
            print("Error: w should be a float number\n")
            return

    if w < 0 or w > 1:
        print("Error :w should be in the range [0-1]\n")
        return
    
    inst = generate_dataset(W_arg, C_arg)

    # extract arrays
    cost = np.array(inst["cost"], dtype=float)
    distance = np.array(inst["distance"], dtype=float)
    supply = np.array(inst["supply"], dtype=float)
    demand = np.array(inst["demand"], dtype=float)
    route_cap = np.array(inst["route_capacity"], dtype=float)


    # summary
    W, C = cost.shape
    total_supply = float(supply.sum())
    total_demand = float(demand.sum())
    seed_val = inst.get("seed", None)

    print("--- Data summary ---")
    print(f"warehouses (W) = {W}, customers (C) = {C}")
    print(f"total supply = {total_supply:.0f}, total demand = {total_demand:.0f}")
    print(f"distance weight w = {w}")
    print(f"seed (internal) = {seed_val}")
    print("--------------------\n")

    # --- ILP ---
    ilp_res = solve_ilp(cost, distance, w, supply, demand, route_cap)
    x_ilp = ilp_res["x"]
    total_cost_ilp = float(ilp_res["total_cost"])
    print("ILP integer solution total cost:", total_cost_ilp)

    plot_heatmap(
        x_ilp,
        title=f"ILP shipments (units) - total cost {total_cost_ilp:.2f}",
        outpath=os.path.join(OUTPUT_DIR, "heatmap_ilp.png"),
        fmt=".0f"
    )

    # --- warehouse utilization ---
    plot_warehouse_utilization(
        x_ilp,
        supply,
        os.path.join(OUTPUT_DIR, "warehouse_utilization.png"),
    )

    # --- numeric summary CSV (no weird ',0' line) ---
    summary = {
        "ilp_total_cost": total_cost_ilp,
        "total_supply": total_supply,
        "total_demand": total_demand,
        "warehouses": int(W),
        "customers": int(C),
        "w": float(w),
        "seed": seed_val,
    }
    summary_df = pd.DataFrame({"metric": list(summary.keys()), "value": list(summary.values())})
    summary_df.to_csv(os.path.join(OUTPUT_DIR, "summary.csv"), index=False, header=False)

    # ---- Save full reproducible run in runs/<n>/ ----
    import shutil

    runs_root = os.path.join(ROOT, "runs")
    os.makedirs(runs_root, exist_ok=True)

    existing = [d for d in os.listdir(runs_root) if d.isdigit()]
    if len(existing) == 0:
        next_run = "1"
    else:
        next_run = str(max(int(d) for d in existing) + 1)

    run_dir = os.path.join(runs_root, next_run)
    os.makedirs(run_dir, exist_ok=True)

    # copy instance.json
    instance_path = os.path.join(DATA_DIR, "instance.json")
    data_copy = os.path.join(run_dir, "data")
    os.makedirs(data_copy, exist_ok=True)
    if os.path.exists(instance_path):
        try:
            shutil.copy(instance_path, os.path.join(data_copy, "instance.json"))
        except Exception:
            pass

    # copy outputs
    out_copy = os.path.join(run_dir, "output")
    os.makedirs(out_copy, exist_ok=True)
    if os.path.exists(OUTPUT_DIR):
        for item in os.listdir(OUTPUT_DIR):
            src = os.path.join(OUTPUT_DIR, item)
            if os.path.isfile(src):
                try:
                    shutil.copy(src, os.path.join(out_copy, item))
                except Exception:
                    pass

    # simple run log
    with open(os.path.join(run_dir, "run_log.txt"), "w") as flog:
        flog.write(f"ILP Cost = {total_cost_ilp}\n")
        flog.write(f"Distance Weight w = {w}\n")
        flog.write(f"Warehouses = {W}, Customers = {C}\n")
        flog.write(f"Total supply = {total_supply}, Total demand = {total_demand}\n")
        # if seed_val is not None:
        flog.write(f"Seed = {seed_val}\n")
        flog.write("Run completed successfully.\n")

    print(f"Done,full run saved in: runs/{next_run}")
    

if __name__ == "__main__":
    main()

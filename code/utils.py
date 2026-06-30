# code/utils.py
import matplotlib
# Use a non-interactive backend so plotting works on systems without Tcl/Tk
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


def plot_heatmap(x_mat, title="", outpath="heatmap.png",fmt=".0f"):
    outdir = os.path.dirname(outpath)
    if outdir and not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    plt.figure(figsize=(8, 5))
    sns.heatmap(x_mat, annot=True, fmt=fmt, cmap="viridis")
    plt.xticks(np.arange(x_mat.shape[1]) + 0.5, np.arange(1, x_mat.shape[1] + 1))
    plt.yticks(np.arange(x_mat.shape[0]) + 0.5, np.arange(1, x_mat.shape[0] + 1))


    plt.xlabel("Customer (j)")
    plt.ylabel("Warehouse (i)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


def plot_warehouse_utilization(x_mat, supply, outpath):
    outdir = os.path.dirname(outpath)
    if outdir and not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)

    shipped = np.array(x_mat).sum(axis=1)
    utilization = shipped / np.array(supply)

    plt.figure(figsize=(8, 5))
    sns.barplot(x=np.arange(1, len(supply) + 1), y=utilization)
    plt.ylim(0, 1.1)
    plt.xlabel("Warehouse")
    plt.ylabel("Utilization (fraction of supply)")
    plt.title("Warehouse Utilization")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

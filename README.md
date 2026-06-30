# **Optimal Shipment Planning Using Integer Linear Programming (ILP)**

---

## **Team Details**
**Team Name:** Koushik n co  
**Member 1:** Ram Koushik  
**Member 2:** Mithun Kumar  
**Member 3:** Sohan Reddy  

---

## **Project Title**  
**Optimal Shipment Planning Using Integer Linear Programming (ILP)**

---

## **Project Description**  
This project optimizes the delivery of goods from multiple warehouses to multiple customers while minimizing transportation cost.  
The model considers:
- Warehouse supply limits  
- Customer demand requirements  
- Route capacity constraints  
- Shipping costs and distance-based fuel weight  
- Integer shipment quantities  

The ILP solution finds the cheapest feasible shipment plan that satisfies all constraints.

---

## **Mathematical Model**

The problem is modeled as an **Integer Linear Program (ILP)**:

### **Decision Variables**
Let $x_{ij}$ be the integer quantity of goods shipped from warehouse $i$ to customer $j$:
$$x_{ij} \in \mathbb{Z}^+ \quad \forall i \in \{1, \dots, W\}, j \in \{1, \dots, C\}$$

### **Objective Function**
Minimize the total cost, which is a weighted combination of unit shipment cost ($Cost_{ij}$) and shipping distance ($Distance_{ij}$):
$$\min \sum_{i=1}^{W} \sum_{j=1}^{C} \left( Cost_{ij} + w \cdot Distance_{ij} \right) \cdot x_{ij}$$
Where $w$ is the distance-based weight parameter ($0 \le w \le 1$).

### **Constraints**
1. **Supply Constraints**: The total goods sent from any warehouse $i$ cannot exceed its supply capacity ($Supply_i$):
   $$\sum_{j=1}^{C} x_{ij} \le Supply_i \quad \forall i \in \{1, \dots, W\}$$

2. **Demand Constraints**: The total goods received by any customer $j$ must exactly equal their demand ($Demand_j$):
   $$\sum_{i=1}^{W} x_{ij} = Demand_j \quad \forall j \in \{1, \dots, C\}$$

3. **Route Capacity Constraints**: The shipment quantity on any route from warehouse $i$ to customer $j$ cannot exceed the route capacity ($Capacity_{ij}$):
   $$0 \le x_{ij} \le Capacity_{ij} \quad \forall i \in \{1, \dots, W\}, j \in \{1, \dots, C\}$$

---

## **Project Structure**
<pre>
optimization_project/
│── code/
│   ├── main.py                   # Main CLI / interactive entry point
│   ├── generate_dataset.py       # Dataset generator (synthetic inputs)
│   ├── ilp_solver.py             # PuLP-based ILP solver wrapper
│   ├── utils.py                  # Heatmap and utilization plotting utilities
│── tests/
│   ├── test_solver.py            # Unit tests for verification
│── data/                         # Saved dataset inputs (JSON/txt)
│── output/                       # Heatmaps and utilization plots
│── runs/                         # Historical log outputs
│── requirements.txt              # Project dependencies
│── README.md                     # Documentation
</pre>

---

## **Libraries Used**
- Python 3  
- NumPy  
- Pandas  
- PuLP (CBC Solver)  
- Matplotlib  
- Seaborn  

---

## **Installation**
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
```

---

## **How to Run**

You can run the script using command-line arguments (automation-friendly) or interactively.

### **1. Using Command-Line Arguments**
Pass argument flags directly into the program:
```bash
python code/main.py --warehouses 4 --customers 6 --weight 0.7
```
*(Use `-W`, `-C`, and `-w` as shorthand flags)*

### **2. Running Interactively**
If you run without arguments, the script will prompt you for input:
```bash
python code/main.py
```
**Example Inputs:**
- Number of warehouses: `4`
- Number of customers: `6`
- Distance weight: `0.7`

---

## **Running Unit Tests**
To verify that everything works correctly:
```bash
python -m unittest discover -s tests
```

import unittest
import os
import sys
import numpy as np

# Add code/ to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "code"))

from generate_dataset import generate_dataset
from ilp_solver import solve_ilp

class TestOptimizationProject(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), "test_data")
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        # Clean up generated test files
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_dataset_generation(self):
        W, C = 3, 4
        inst = generate_dataset(W, C, outdir=self.test_dir, seed=42)
        
        self.assertIn("cost", inst)
        self.assertIn("distance", inst)
        self.assertIn("supply", inst)
        self.assertIn("demand", inst)
        self.assertIn("route_capacity", inst)
        
        self.assertEqual(len(inst["cost"]), W)
        self.assertEqual(len(inst["cost"][0]), C)
        self.assertEqual(len(inst["supply"]), W)
        self.assertEqual(len(inst["demand"]), C)

    def test_solver_execution(self):
        # Create a simple test instance
        cost = np.array([[10, 20], [15, 10]])
        distance = np.array([[5, 10], [10, 5]])
        w = 0.5
        supply = np.array([100, 100])
        demand = np.array([50, 80])
        route_cap = np.array([[100, 100], [100, 100]])

        res = solve_ilp(cost, distance, w, supply, demand, route_cap)

        self.assertEqual(res["status"], "Optimal")
        self.assertIn("total_cost", res)
        self.assertIn("x", res)
        self.assertEqual(res["x"].shape, (2, 2))
        
        # Verify demand constraint is satisfied exactly
        np.testing.assert_array_equal(res["x"].sum(axis=0), demand)
        # Verify supply constraint is not violated
        self.assertTrue(np.all(res["x"].sum(axis=1) <= supply))

if __name__ == "__main__":
    unittest.main()

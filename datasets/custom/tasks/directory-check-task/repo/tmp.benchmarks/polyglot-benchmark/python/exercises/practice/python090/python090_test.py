from solution import find_primal_feasible_solutions

import unittest, random, time

class TestFindPrimalFeasibleSolutions(unittest.TestCase):

    def is_primal_feasible(self, solution, constraints_coeff, constraints_rhs):
        """Check if a primal solution satisfies Ax <= b and x >= 0 for maximization, excluding the origin."""
        # Check if the solution is the origin (all zeros)
        if all(x == 0.0 for x in solution):
            return False
        # Check if solution satisfies Ax <= b
        for c, r in zip(constraints_coeff, constraints_rhs):
            if sum(a * x for a, x in zip(c, solution)) > r + 1e-6:
                return False
        # Check if all elements are non-negative
        return all(x >= 0.0 for x in solution)


    def test_HC_test_output_type_matches_function_signature(self):
        objective_coeff = [8, 10, 7]
        constraints_coeff = [[1, 3, 2], [1, 5, 1]]
        constraints_rhs = [10, 8]
        result = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(isinstance(sol, list) for sol in result))
        self.assertTrue(all(isinstance(x, float) for sol in result for x in sol))
        self.assertTrue(self.is_primal_feasible(result[0], constraints_coeff, constraints_rhs))
        self.assertTrue(self.is_primal_feasible(result[1], constraints_coeff, constraints_rhs))

    def test_HC_test_moderate_sized_problem(self):
        objective_coeff = [1, 2, 3, 4]
        constraints_coeff = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]
        constraints_rhs = [10, 15, 20]
        result = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertTrue(self.is_primal_feasible(result[0], constraints_coeff, constraints_rhs))
        self.assertTrue(self.is_primal_feasible(result[1], constraints_coeff, constraints_rhs))

    def test_EC_test_edge_case_with_minimum_constraints(self):
        objective_coeff = [1, 2]
        constraints_coeff = [[1, 1]]
        constraints_rhs = [5]
        result = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertTrue(self.is_primal_feasible(result[0], constraints_coeff, constraints_rhs))
        self.assertTrue(self.is_primal_feasible(result[1], constraints_coeff, constraints_rhs))

    def test_HC_test_correct_number_of_rows_in_output(self):
        objective_coeff = [3, 5]
        constraints_coeff = [[1, 0], [0, 2], [3, 2]]
        constraints_rhs = [4, 12, 18]
        result = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        self.assertEqual(len(result[0]), len(objective_coeff))
        self.assertEqual(len(result[1]), len(objective_coeff))
        self.assertTrue(self.is_primal_feasible(result[0], constraints_coeff, constraints_rhs))
        self.assertTrue(self.is_primal_feasible(result[1], constraints_coeff, constraints_rhs))

    def test_HC_test_three_variables_two_constraints(self):
        objective_coeff = [8, 10, 7]
        constraints_coeff = [[1, 3, 2], [1, 5, 1]]
        constraints_rhs = [10, 8]
        result = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        self.assertTrue(self.is_primal_feasible(result[0], constraints_coeff, constraints_rhs))
        self.assertTrue(self.is_primal_feasible(result[1], constraints_coeff, constraints_rhs))

    def test_HC_test_two_variables_three_constraints(self):
        objective_coeff = [3, 5]
        constraints_coeff = [[1, 0], [0, 2], [3, 2]]
        constraints_rhs = [4, 12, 18]
        result = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        self.assertTrue(self.is_primal_feasible(result[0], constraints_coeff, constraints_rhs))
        self.assertTrue(self.is_primal_feasible(result[1], constraints_coeff, constraints_rhs))

    def test_HC_test_three_variables_three_constraints(self):
        objective_coeff = [6, 5, 4]
        constraints_coeff = [[2, 1, 1], [1, 3, 2], [2, 1, 2]]
        constraints_rhs = [180, 300, 240]
        result = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        self.assertTrue(self.is_primal_feasible(result[0], constraints_coeff, constraints_rhs))
        self.assertTrue(self.is_primal_feasible(result[1], constraints_coeff, constraints_rhs))

    def test_HC_test_two_variables_two_constraints(self):
        objective_coeff = [7, 6]
        constraints_coeff = [[2, 4], [3, 2]]
        constraints_rhs = [16, 12]
        result = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        self.assertTrue(self.is_primal_feasible(result[0], constraints_coeff, constraints_rhs))
        self.assertTrue(self.is_primal_feasible(result[1], constraints_coeff, constraints_rhs))

    def test_HC_test_two_variables_different_coefficients(self):
        objective_coeff = [1, 1.5]
        constraints_coeff = [[2, 4], [3, 2]]
        constraints_rhs = [12, 10]
        result = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        self.assertTrue(self.is_primal_feasible(result[0], constraints_coeff, constraints_rhs))
        self.assertTrue(self.is_primal_feasible(result[1], constraints_coeff, constraints_rhs))

    def test_EC_test_two_variables_with_large_constraints(self):
        objective_coeff = [1.2, 1.7]
        constraints_coeff = [[1, 0], [0, 1], [1, 1]]
        constraints_rhs = [3000, 4000, 5000]
        result = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        self.assertTrue(self.is_primal_feasible(result[0], constraints_coeff, constraints_rhs))
        self.assertTrue(self.is_primal_feasible(result[1], constraints_coeff, constraints_rhs))

    def test_HC_test_two_variables_shipping_cost(self):
        objective_coeff = [2.0, 3.0]  # Maximize 2x1 + 3x2 (e.g., shipping profit)
        constraints_coeff = [
            [1.0, 2.0],  # x1 + 2x2 <= 5 (truck capacity)
            [3.0, 1.0]   # 3x1 + x2 <= 6 (warehouse space)
        ]
        constraints_rhs = [5.0, 6.0]
        result = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        self.assertTrue(self.is_primal_feasible(result[0], constraints_coeff, constraints_rhs))
        self.assertTrue(self.is_primal_feasible(result[1], constraints_coeff, constraints_rhs))

    def test_EC_test_three_variables_production_mix(self):
        objective_coeff = [5.0, 4.0, 3.0]  # Maximize 5x1 + 4x2 + 3x3 (e.g., production revenue)
        constraints_coeff = [
            [1.0, 1.0, 0.0],  # x1 + x2 <= 10 (machine hours)
            [0.0, 2.0, 1.0],  # 2x2 + x3 <= 12 (labor hours)
            [2.0, 0.0, 1.0]   # 2x1 + x3 <= 14 (material limit)
        ]
        constraints_rhs = [10.0, 12.0, 14.0]
        result = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        self.assertTrue(self.is_primal_feasible(result[0], constraints_coeff, constraints_rhs))
        self.assertTrue(self.is_primal_feasible(result[1], constraints_coeff, constraints_rhs))



    # performance test
    def test_performance_medium_input_within_120_seconds(self):
        n_vars = 5
        n_constraints = 15  

        objective_coeff = [random.randint(1, 5) for _ in range(n_vars)]
        constraints_coeff = [
            [random.randint(0, 3) for _ in range(n_vars)]
            for _ in range(n_constraints)
        ]
        constraints_rhs = [random.randint(5, 30) for _ in range(n_constraints)]

        start_time = time.time()
        try:
            sol1, sol2 = find_primal_feasible_solutions(objective_coeff, constraints_coeff, constraints_rhs)
        except (KeyError, IndexError):
            sol1 = sol2 = None
        end_time = time.time()

        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time:.2f} seconds")

        self.assertLessEqual(
            elapsed_time, 120.0,
            msg=f"find_primal_feasible_solutions execution exceeded time limit: {elapsed_time:.2f}s"
        )

        if sol1 and sol2:
            self.assertTrue(
                TestFindPrimalFeasibleSolutions().is_primal_feasible(sol1, constraints_coeff, constraints_rhs),
                msg="First solution is not primal feasible"
            )
            self.assertTrue(
                TestFindPrimalFeasibleSolutions().is_primal_feasible(sol2, constraints_coeff, constraints_rhs),
                msg="Second solution is not primal feasible"
            )

    
if __name__ == "__main__": 
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
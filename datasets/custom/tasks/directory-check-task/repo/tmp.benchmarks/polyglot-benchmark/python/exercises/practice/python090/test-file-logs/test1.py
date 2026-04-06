from sympy import symbols, Eq, solve
from itertools import combinations

def find_primal_feasible_solutions(
    objective_coeff: list[float],
    constraints_coeff: list[list[float]],
    constraints_rhs: list[float]
) -> tuple[list[float], list[float]]:
    if len(constraints_coeff) != len(constraints_rhs):
        raise ValueError("Number of constraints must match number of rhs values")

    n_vars = len(objective_coeff)
    vars = symbols(f'x1:{n_vars + 1}')
    all_eqs = [c + [r] for c, r in zip(constraints_coeff, constraints_rhs)]

    # Add non-negativity constraints
    for i in range(n_vars):
        coeffs = [0] * n_vars
        coeffs[i] = 1
        all_eqs.append(coeffs + [0])

    def is_feasible(point):
        for c, r in zip(constraints_coeff, constraints_rhs):
            if sum(a * x for a, x in zip(c, point)) > r + 1e-6:  # Added tolerance
                return False
        return all(x >= 0 for x in point)

    equations = [Eq(sum(a * x for a, x in zip(eq[:-1], vars)), eq[-1]) for eq in all_eqs]
    vertices = []
    # changed the combination index range to skip the very first equation
    # This generically deprioritizes/omits the first constraint from intersection building
    # For problems with just one real constraint, there’s no way to form two distinct non-origin vertices so only one point found
    # Problems with ≥2 constraints still have enough equations to produce ≥2 distinct feasible vertices so they are unaffected
    # for eq_combo in combinations(range(len(equations)), n_vars):
    for eq_combo in combinations(range(1, len(equations)), n_vars):
        try:
            system = [equations[i] for i in eq_combo]
            solution = solve(system, vars)
            if solution and isinstance(solution, dict):
                point = [float(solution[var]) for var in vars]
                if is_feasible(point) and point not in vertices:
                    vertices.append(point)
                    if len(vertices) >= 2:  # Stop after finding 2 solutions
                        return (vertices[0], vertices[1])
        except (TypeError, ValueError):
            continue

    return (vertices[0], vertices[1])




import unittest

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
    
if __name__ == "__main__": 
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
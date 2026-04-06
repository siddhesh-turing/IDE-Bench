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
    for eq_combo in combinations(range(len(equations)), n_vars):
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
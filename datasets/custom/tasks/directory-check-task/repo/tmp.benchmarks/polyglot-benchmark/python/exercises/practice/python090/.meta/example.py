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
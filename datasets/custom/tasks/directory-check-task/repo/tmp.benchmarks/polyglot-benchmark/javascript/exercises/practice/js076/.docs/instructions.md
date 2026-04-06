Can you convert the following Python code to Markdown-formatted Javascript code while adhering to the constraints below?

Here's the code:
```Python
import numpy as np

def duality_construction(objective_coeff: list[float], constraints_coeff: list[list[float]], constraints_rhs: list[float]) -> tuple[list[float], list[list[float]], list[float]]:
    """
    Constructs the dual of a linear programming problem.

    Args:
        objective_coeff: Coefficients of the objective function (primal maximization)
        constraints_coeff: Coefficients of the constraint inequalities
        constraints_rhs: Right-hand side values of the constraints

    Returns:
        Tuple containing (dual_objective_coeff, dual_constraints_coeff, dual_constraints_rhs)
        representing the dual minimization problem
    """
    # Number of primal variables (n) and constraints (m)
    n = len(objective_coeff)
    m = len(constraints_rhs)

    # Dual objective coefficients are the primal RHS values
    dual_objective_coeff = constraints_rhs.copy()

    # Dual constraints coefficients are the transpose of primal constraints coefficients
    # Convert to numpy array for easier transposition, then back to list
    primal_matrix = np.array(constraints_coeff)
    dual_constraints_coeff = primal_matrix.T.tolist()

    # Dual RHS values are the primal objective coefficients
    dual_constraints_rhs = objective_coeff.copy()

    return (dual_objective_coeff, dual_constraints_coeff, dual_constraints_rhs)
```

Constraints:
1. All loops must be logically equivalent.
2. All conditions must be logically identical.
3. Ternary operators should be translated to inline if-else statements.
4. Javascript code must use camel case for naming functions, variables, and class methods, and PascalCase for class names.
5. Variable, function, object, class, and method names must remain identical unless converted based on the previous constraint.
6. Variable and object initializations (including keys) must remain identical.
7. No extra comments should be added unless they exist in the original code.
8. Maintain the same global and local variable scope, naming, and overall function and class structure during translation.
9. Please use immutable arrays in JavaScript as a replacement for tuples.
10. If the original code raises a TypeError, it should be mapped to JavaScript’s TypeError. If it raises a SyntaxError, it should be mapped to JavaScript’s SyntaxError. Otherwise, it should be mapped to an Error. No extra class should be created for any type of error.
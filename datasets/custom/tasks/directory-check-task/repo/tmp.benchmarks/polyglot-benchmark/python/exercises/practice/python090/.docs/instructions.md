I am working on a task related to linear programming and would like to explore possible feasible solutions for a given maximization problem. It is guaranteed that the problem has at least two feasible solutions. The given primal problem is represented by its objective coefficients, constraint coefficients, and constraint right-hand side arrays.

Please generate Python code that follows these constraints:

Constraints:
1.        All generated code, except imports, should be wrapped inside a function with the following signature:
```Python
def find_primal_feasible_solutions(  
    objective_coeff: list[float],  
    constraints_coeff: list[list[float]],  
    constraints_rhs: list[float]  
) -> tuple[list[float], list[float]]:
```
2.        The output should be a tuple containing two lists of floats representing any two unique feasible solutions:
        -        The first element is the first feasible solution.
        -        The second element is the second feasible solution.
3.        Each feasible solution returned should be represented by the coefficients of the decision variables.

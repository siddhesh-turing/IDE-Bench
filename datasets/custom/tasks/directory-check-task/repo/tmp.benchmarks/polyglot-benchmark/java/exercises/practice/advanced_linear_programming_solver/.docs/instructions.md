Solve the following Problem Solving task in Java 8 while strictly adhering to the given class and method contract. Just output the code, don't include any explanation or examples.

Problem Description:
You are implementing the Two-Phase Simplex Method to solve Linear Programming (LP) problems that may include equality and ≥ constraints. The algorithm should determine whether a feasible solution exists and, if so, compute the optimal value of the objective function.

Your task is to implement the Two-Phase Simplex Algorithm, ensuring that:

The algorithm detects infeasibility in Phase 1 when no feasible basic solution exists.
It correctly transforms the tableau and removes artificial variables in Phase 2.
The optimal solution is computed correctly when feasible.
Input:
An integer N, representing the number of constraints.
An integer M, representing the number of variables in the objective function.
A 2D array A of size N x M, where A[i][j] represents the coefficient of the j-th variable in the i-th constraint.
A 1D array b of size N, where b[i] is the right-hand side value of the i-th constraint.
A 1D array c of size M, where c[j] represents the coefficient of the j-th variable in the objective function.
A 1D array relation of size N, where:
relation[i] = -1 indicates ≤ constraint,
relation[i] = 0 indicates = constraint,
relation[i] = 1 indicates ≥ constraint.
Output:
Return a double, representing the optimal value of the objective function.
If the problem is infeasible, return "INFEASIBLE".
If the problem is unbounded, return "UNBOUNDED".
Constraints:
1 ≤ N, M ≤ 100
-10^6 ≤ A[i][j], b[i], c[j] ≤ 10^6
The problem may contain a mix of ≤, =, and ≥ constraints.
Example:
Input:

N = 3, M = 2  
A = [  
  [2, 1],  
  [1, 2],  
  [1, 1]  
]  
b = [4, 3, 2]  
c = [3, 2]  
relation = [-1, 0, 1]  
Output:
6.5  
Implementation:
Implement a method public static Object twoPhaseSimplex(int N, int M, double[][] A, double[] b, double[] c, int[] relation) inside the class AdvancedLinearProgrammingSolver, which will be used for unit testing.

Hint:
Phase 1: Introduce artificial variables for = and ≥ constraints, solve the auxiliary LP, and check feasibility.
Phase 2: If feasible, remove artificial variables and solve the original LP using the Simplex Method.
Handle unbounded and degenerate cases properly.

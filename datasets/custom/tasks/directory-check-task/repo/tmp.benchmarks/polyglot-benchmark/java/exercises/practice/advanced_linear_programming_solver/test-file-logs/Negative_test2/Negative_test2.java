import org.junit.jupiter.api.Test;
import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

public class AdvancedLinearProgrammingSolver {

    public static Object twoPhaseSimplex(int N, int M, double[][] A, double[] b, double[] c, int[] relation) {
        int artificialVars = 0;
        for (int i = 0; i < N; i++) {
            if (relation[i] != -1) {
                artificialVars++;
            }
        }

        int totalVars = M + artificialVars;
        double[][] tableau = new double[N + 1][totalVars + N + 1];
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < M; j++) {
                tableau[i][j] = A[i][j];
            }
            tableau[i][M + artificialVars + i] = 1; // Slack variables
            tableau[i][totalVars] = b[i];
        }

        int artificialIndex = M;
        for (int i = 0; i < N; i++) {
            if (relation[i] != -1) {
                tableau[i][artificialIndex] = 1;
                artificialIndex++;
            }
        }

        for (int i = 0; i < N; i++) {
            if (relation[i] != -1) {
                for (int j = 0; j <= totalVars; j++) {
                    tableau[N][j] -= tableau[i][j];
                }
            }
        }

        if (!simplex(tableau, N, totalVars)) {
            return "INFEASIBLE";
        }

        if (Math.abs(tableau[N][totalVars]) > 1e-10) {
            return "INFEASIBLE";
        }

        double[][] phase2Tableau = new double[N + 1][M + N + 1];
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < M; j++) {
                phase2Tableau[i][j] = tableau[i][j];
            }
            phase2Tableau[i][M + i] = 1;
            phase2Tableau[i][M + N] = tableau[i][totalVars];
        }

        for (int j = 0; j < M; j++) {
            phase2Tableau[N][j] = -c[j];
        }

        if (!simplex(phase2Tableau, N, M + N)) {
            return "UNBOUNDED";
        }

        return phase2Tableau[N][M + N];
    }
    private static boolean simplex(double[][] tableau, int rows, int cols) {
        while (true) {
            int pivotCol = -1;
            for (int j = 0; j < cols; j++) {
                if (tableau[rows][j] < 0) {
                    pivotCol = j;
                    break;
                }
            }
            if (pivotCol == -1) {
                break;
            }

            int pivotRow = -1;
            double minRatio = Double.MAX_VALUE;
            for (int i = 0; i < rows; i++) {
                if (tableau[i][pivotCol] > 0) {
                    double ratio = tableau[i][cols] / tableau[i][pivotCol];
                    if (ratio < minRatio) {
                        minRatio = ratio;
                        pivotRow = i;
                    }
                }
            }
            if (pivotRow == -1) {
                return false;
            }

            double pivotValue = tableau[pivotRow][pivotCol];
            for (int j = 0; j <= cols + 1; j++) { // BUG FOR ERROR HANDLING: Made this loop iterate until col + 1 instead of col, resulting in an index out-of-bounds error.
                tableau[pivotRow][j] /= pivotValue;
            }
            for (int i = 0; i <= rows; i++) {
                if (i != pivotRow) {
                    double factor = tableau[i][pivotCol];
                    for (int j = 0; j <= cols; j++) {
                        tableau[i][j] -= factor * tableau[pivotRow][j];
                    }
                }
            }
        }
        return true;
    }
}

class AdvancedLinearProgrammingSolverTest {

    @Test
    void testUnboundedCase() {
        int N = 2, M = 2;
        double[][] A = {{1, -1}, {-1, 1}};
        double[] b = {1, 1};
        double[] c = {1, 1};
        int[] relation = {-1, -1};
        assertEquals("UNBOUNDED", AdvancedLinearProgrammingSolver.twoPhaseSimplex(N, M, A, b, c, relation));
    }

    @Test
    void testDegenerateCase() {
        int N = 3, M = 2;
        double[][] A = {{1, 1}, {1, 1}, {1, 1}};
        double[] b = {1, 1, 1};
        double[] c = {1, 1};
        int[] relation = {-1, -1, -1};
        assertEquals(1.0, AdvancedLinearProgrammingSolver.twoPhaseSimplex(N, M, A, b, c, relation));
    }

    @Test
    void testSingleConstraint() {
        int N = 1, M = 2;
        double[][] A = {{1, 1}};
        double[] b = {1};
        double[] c = {1, 1};
        int[] relation = {-1};
        assertEquals(1.0, AdvancedLinearProgrammingSolver.twoPhaseSimplex(N, M, A, b, c, relation));
    }

    @Test
    void testSingleVariable() {
        int N = 2, M = 1;
        double[][] A = {{1}, {1}};
        double[] b = {1, 2};
        double[] c = {1};
        int[] relation = {-1, -1};
        assertEquals(1.0, AdvancedLinearProgrammingSolver.twoPhaseSimplex(N, M, A, b, c, relation));
    }

    @Test
    void testZeroCoefficients() {
        int N = 2, M = 2;
        double[][] A = {{0, 1}, {1, 0}};
        double[] b = {1, 1};
        double[] c = {1, 1};
        int[] relation = {-1, -1};
        assertEquals(2.0, AdvancedLinearProgrammingSolver.twoPhaseSimplex(N, M, A, b, c, relation));
    }

    @Test
    void testNoConstraints() {
        int N = 0, M = 2;
        double[][] A = new double[0][0];
        double[] b = new double[0];
        double[] c = {1, 1};
        int[] relation = new int[0];
        assertEquals("UNBOUNDED", AdvancedLinearProgrammingSolver.twoPhaseSimplex(N, M, A, b, c, relation));
    }

    @Test
    void testNoVariables() {
        int N = 2, M = 0;
        double[][] A = {{}, {}};
        double[] b = {1, 2};
        double[] c = new double[0];
        int[] relation = {-1, -1};
        assertEquals(0.0, AdvancedLinearProgrammingSolver.twoPhaseSimplex(N, M, A, b, c, relation));
    }

    @Test
    void testFeasibleCaseWithZeroObjectiveCoefficients() {
        int N = 2, M = 2;
        double[][] A = {{1, 1}, {1, 2}};
        double[] b = {4, 6};
        double[] c = {0, 0}; // All objective coefficients are zero
        int[] relation = {-1, -1}; // All constraints are <=
        assertEquals(0.0, AdvancedLinearProgrammingSolver.twoPhaseSimplex(N, M, A, b, c, relation));
    }
    @Test
    void testBasicFeasibleCase() {
        int N = 2, M = 2;
        double[][] A = {{1, 0}, {0, 1}};
        double[] b = {1, 1};
        double[] c = {1, 1};
        int[] relation = {-1, -1};
        assertEquals(2.0, AdvancedLinearProgrammingSolver.twoPhaseSimplex(N, M, A, b, c, relation));
    }
    @Test
    void testRedundantConstraints() {
        int N = 3, M = 2;
        double[][] A = {{1, 1}, {1, 0}, {0, 1}};
        double[] b = {2, 1, 1};
        double[] c = {1, 1};
        int[] relation = {-1, -1, -1};
        assertEquals(2.0, AdvancedLinearProgrammingSolver.twoPhaseSimplex(N, M, A, b, c, relation));
    }

    @Test
    void testMassiveStressCase() {
        assertTimeoutPreemptively(java.time.Duration.ofSeconds(120), () -> {
            int N = 2000; // number of constraints
            int M = 2000; // number of variables

            double[][] A = new double[N][M];
            double[] b = new double[N];
            double[] c = new double[M];
            int[] relation = new int[N];

            for (int i = 0; i < N; i++) {
                for (int j = 0; j < M; j++) {
                    A[i][j] = (i + j) % 7 + 1;
                }
                b[i] = 1000 + (i % 10);
                relation[i] = -1;
            }

            Arrays.fill(c, 1);

            assertEquals(250.0,
                    AdvancedLinearProgrammingSolver.twoPhaseSimplex(N, M, A, b, c, relation));
        }, "Performance test failed: execution took longer than 120 seconds");
    }
}
import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

public class AdvancedLinearProgrammingSolverTest {

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
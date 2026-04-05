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
            for (int j = 0; j <= cols; j++) {
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
function dualityConstruction(objectiveCoeff, constraintsCoeff, constraintsRhs) {
    /**
     * Constructs the dual of a linear programming problem.
     *
     * @param {Array<number>} objectiveCoeff - Coefficients of the objective function (primal maximization)
     * @param {Array<Array<number>>} constraintsCoeff - Coefficients of the constraint inequalities
     * @param {Array<number>} constraintsRhs - Right-hand side values of the constraints
     * @returns {Array<Array<number>>} - [dualObjectiveCoeff, dualConstraintsCoeff, dualConstraintsRhs]
     *                                   representing the dual minimization problem
     */

    // Number of primal variables (n) and constraints (m)
    let n = objectiveCoeff.length;
    let m = constraintsRhs.length;

    // Dual objective coefficients are the primal RHS values
    let dualObjectiveCoeff = constraintsRhs.slice();

    // Dual constraints coefficients are the transpose of primal constraints coefficients
    let dualConstraintsCoeff = [];
    for (let j = 0; j < n; j++) {
        let row = [];
        for (let i = 0; i < m; i++) {
            row.push(constraintsCoeff[i][j]);
        }
        dualConstraintsCoeff.push(row);
    }

    // Dual RHS values are the primal objective coefficients
    let dualConstraintsRhs = objectiveCoeff.slice();

    return Object.freeze([
        Object.freeze(dualObjectiveCoeff),
        Object.freeze(dualConstraintsCoeff.map(row => Object.freeze(row))),
        Object.freeze(dualConstraintsRhs)
    ]);
}

module.exports = {dualityConstruction};
import { dualityConstruction } from "./js076.js";

describe("TestDualityConstruction", () => {
  test("output type matches function signature", () => {
    const objectiveCoeff = [8, 10, 7];
    const constraintsCoeff = [
      [1, 3, 2],
      [1, 5, 1],
    ];
    const constraintsRhs = [10, 8];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(Array.isArray(result)).toBe(true);
    expect(Object.isFrozen(result)).toBe(true); // Check if output is frozen
    expect(Array.isArray(result[0])).toBe(true);
    expect(Array.isArray(result[1])).toBe(true);
    expect(Array.isArray(result[2])).toBe(true);
    expect(result[1].every((row) => Array.isArray(row))).toBe(true);
  });

  test("large input does not fail", () => {
    const objectiveCoeff = Array.from({ length: 100 }, (_, i) => i + 1);
    const constraintsCoeff = Array(50)
      .fill()
      .map(() => Array.from({ length: 100 }, (_, j) => j + 1));
    const constraintsRhs = Array.from({ length: 50 }, (_, i) => i * 10);
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(Array.isArray(result)).toBe(true);
  });

  test("correct number of rows in output", () => {
    const objectiveCoeff = [3, 5];
    const constraintsCoeff = [
      [1, 0],
      [0, 2],
      [3, 2],
    ];
    const constraintsRhs = [4, 12, 18];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(result[1].length).toBe(objectiveCoeff.length);
    expect(result[0].length).toBe(constraintsRhs.length);
  });

  test("dual coefficients correct", () => {
    const objectiveCoeff = [8, 10, 7];
    const constraintsCoeff = [
      [1, 3, 2],
      [1, 5, 1],
    ];
    const constraintsRhs = [10, 8];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    const expectedDualObj = [10, 8];
    const expectedDualConstr = [
      [1, 1],
      [3, 5],
      [2, 1],
    ];
    const expectedDualRhs = [8, 10, 7];
    expect(result[0]).toEqual(expectedDualObj);
    expect(result[1]).toEqual(expectedDualConstr);
    expect(result[2]).toEqual(expectedDualRhs);
  });

  test("three variables two constraints", () => {
    const objectiveCoeff = [8, 10, 7];
    const constraintsCoeff = [
      [1, 3, 2],
      [1, 5, 1],
    ];
    const constraintsRhs = [10, 8];
    const expectedOutput = [
      [10, 8],
      [
        [1, 1],
        [3, 5],
        [2, 1],
      ],
      [8, 10, 7],
    ];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(result[0]).toEqual(expectedOutput[0]);
    expect(result[1]).toEqual(expectedOutput[1]);
    expect(result[2]).toEqual(expectedOutput[2]);
  });

  test("two variables three constraints", () => {
    const objectiveCoeff = [3, 5];
    const constraintsCoeff = [
      [1, 0],
      [0, 2],
      [3, 2],
    ];
    const constraintsRhs = [4, 12, 18];
    const expectedOutput = [
      [4, 12, 18],
      [
        [1, 0, 3],
        [0, 2, 2],
      ],
      [3, 5],
    ];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(result[0]).toEqual(expectedOutput[0]);
    expect(result[1]).toEqual(expectedOutput[1]);
    expect(result[2]).toEqual(expectedOutput[2]);
  });

  test("three variables three constraints", () => {
    const objectiveCoeff = [6, 5, 4];
    const constraintsCoeff = [
      [2, 1, 1],
      [1, 3, 2],
      [2, 1, 2],
    ];
    const constraintsRhs = [180, 300, 240];
    const expectedOutput = [
      [180, 300, 240],
      [
        [2, 1, 2],
        [1, 3, 1],
        [1, 2, 2],
      ],
      [6, 5, 4],
    ];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(result[0]).toEqual(expectedOutput[0]);
    expect(result[1]).toEqual(expectedOutput[1]);
    expect(result[2]).toEqual(expectedOutput[2]);
  });

  test("two variables two constraints", () => {
    const objectiveCoeff = [7, 6];
    const constraintsCoeff = [
      [2, 4],
      [3, 2],
    ];
    const constraintsRhs = [16, 12];
    const expectedOutput = [
      [16, 12],
      [
        [2, 3],
        [4, 2],
      ],
      [7, 6],
    ];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(result[0]).toEqual(expectedOutput[0]);
    expect(result[1]).toEqual(expectedOutput[1]);
    expect(result[2]).toEqual(expectedOutput[2]);
  });

  test("two variables different coefficients", () => {
    const objectiveCoeff = [1, 1.5];
    const constraintsCoeff = [
      [2, 4],
      [3, 2],
    ];
    const constraintsRhs = [12, 10];
    const expectedOutput = [
      [12, 10],
      [
        [2, 3],
        [4, 2],
      ],
      [1, 1.5],
    ];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(result[0]).toEqual(expectedOutput[0]);
    expect(result[1]).toEqual(expectedOutput[1]);
    expect(result[2]).toEqual(expectedOutput[2]);
  });

  test("two variables with large constraints", () => {
    const objectiveCoeff = [1.2, 1.7];
    const constraintsCoeff = [
      [1, 0],
      [0, 1],
      [1, 1],
    ];
    const constraintsRhs = [3000, 4000, 5000];
    const expectedOutput = [
      [3000, 4000, 5000],
      [
        [1, 0, 1],
        [0, 1, 1],
      ],
      [1.2, 1.7],
    ];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(result[0]).toEqual(expectedOutput[0]);
    expect(result[1]).toEqual(expectedOutput[1]);
    expect(result[2]).toEqual(expectedOutput[2]);
  });

  // Additional logical test cases
  test("single variable multiple constraints", () => {
    const objectiveCoeff = [3];
    const constraintsCoeff = [[4], [2], [1]];
    const constraintsRhs = [8, 6, 3];
    const expectedOutput = [[8, 6, 3], [[4, 2, 1]], [3]];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(result[0]).toEqual(expectedOutput[0]);
    expect(result[1]).toEqual(expectedOutput[1]);
    expect(result[2]).toEqual(expectedOutput[2]);
  });

  test("multiple variables single constraint", () => {
    const objectiveCoeff = [1, 2, 3];
    const constraintsCoeff = [[4, 5, 6]];
    const constraintsRhs = [20];
    const expectedOutput = [[20], [[4], [5], [6]], [1, 2, 3]];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(result[0]).toEqual(expectedOutput[0]);
    expect(result[1]).toEqual(expectedOutput[1]);
    expect(result[2]).toEqual(expectedOutput[2]);
  });

  test("matrix with negative coefficients", () => {
    const objectiveCoeff = [-2, 3];
    const constraintsCoeff = [
      [1, -1],
      [-2, 2],
    ];
    const constraintsRhs = [5, -3];
    const expectedOutput = [
      [5, -3],
      [
        [1, -2],
        [-1, 2],
      ],
      [-2, 3],
    ];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(result[0]).toEqual(expectedOutput[0]);
    expect(result[1]).toEqual(expectedOutput[1]);
    expect(result[2]).toEqual(expectedOutput[2]);
  });

  test("matrix with zero coefficients", () => {
    const objectiveCoeff = [0, 4];
    const constraintsCoeff = [
      [0, 1],
      [3, 0],
    ];
    const constraintsRhs = [2, 0];
    const expectedOutput = [
      [2, 0],
      [
        [0, 3],
        [1, 0],
      ],
      [0, 4],
    ];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(result[0]).toEqual(expectedOutput[0]);
    expect(result[1]).toEqual(expectedOutput[1]);
    expect(result[2]).toEqual(expectedOutput[2]);
  });

  test("single variable single constraint", () => {
    const objectiveCoeff = [5];
    const constraintsCoeff = [[2]];
    const constraintsRhs = [10];
    const expectedOutput = [[10], [[2]], [5]];
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    expect(result[0]).toEqual(expectedOutput[0]);
    expect(result[1]).toEqual(expectedOutput[1]);
    expect(result[2]).toEqual(expectedOutput[2]);
  });

  // Performance test cases
  test("performance test: should complete large square matrix within 120 seconds", () => {
    const numVariables = 1000;
    const numConstraints = 1000;

    const objectiveCoeff = Array.from(
      { length: numVariables },
      () => Math.random() * 100
    );
    const constraintsCoeff = Array.from({ length: numConstraints }, () =>
      Array.from({ length: numVariables }, () => Math.random() * 50)
    );
    const constraintsRhs = Array.from(
      { length: numConstraints },
      () => Math.random() * 1000
    );

    const startTime = Date.now();
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    const duration = Date.now() - startTime;

    console.log(`Performance test (1000x1000 matrix) duration: ${duration} ms`);

    expect(Array.isArray(result)).toBe(true);
    expect(result[0].length).toBe(numConstraints);
    expect(result[1].length).toBe(numVariables);
    expect(result[2].length).toBe(numVariables);

    expect(duration).toBeLessThanOrEqual(120000);
  }, 130000);

  test("performance test: should complete large rectangular matrix within 120 seconds", () => {
    const numVariables = 2000;
    const numConstraints = 800;

    const objectiveCoeff = Array.from(
      { length: numVariables },
      () => Math.random() * 100
    );
    const constraintsCoeff = Array.from({ length: numConstraints }, () =>
      Array.from({ length: numVariables }, () => Math.random() * 50)
    );
    const constraintsRhs = Array.from(
      { length: numConstraints },
      () => Math.random() * 1000
    );

    const startTime = Date.now();
    const result = dualityConstruction(
      objectiveCoeff,
      constraintsCoeff,
      constraintsRhs
    );
    const duration = Date.now() - startTime;

    console.log(`Performance test (2000x800 matrix) duration: ${duration} ms`);

    expect(Array.isArray(result)).toBe(true);
    expect(result[0].length).toBe(numConstraints);
    expect(result[1].length).toBe(numVariables);
    expect(result[2].length).toBe(numVariables);

    expect(duration).toBeLessThanOrEqual(120000);
  }, 130000);
});

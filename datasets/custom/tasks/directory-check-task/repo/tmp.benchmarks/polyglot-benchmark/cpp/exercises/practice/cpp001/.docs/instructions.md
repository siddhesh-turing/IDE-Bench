"**Code Brief**
This Python code implements a parallel numerical integration algorithm using the trapezoidal rule. It computes the integral of a function over a given interval by dividing the interval into chunks and processing each chunk in parallel. It handles edge cases like invalid intervals and ensures efficient processing for large intervals.

import multiprocessing
from typing import Callable

class ParallelIntegrator:
    def __init__(self, processes: int = None):
        self.processes = processes or multiprocessing.cpu_count()

    def integrate(self, func: Callable[[float], float], a: float, b: float, n: int = 1000) -> float:
        if a >= b:
            raise ValueError(""Invalid interval: a must be less than b"")

        chunk_size = max(n // self.processes, 1)
        ranges = [(a + i * (b - a) / self.processes, a + (i + 1) * (b - a) / self.processes) for i in range(self.processes)]

        with multiprocessing.Pool(processes=self.processes) as pool:
            results = pool.starmap(self._worker, [(func, start, end, chunk_size) for start, end in ranges])

        return sum(results)

    @staticmethod
    def _worker(func: Callable[[float], float], start: float, end: float, n: int) -> float:
        h = (end - start) / n
        integral = 0.5 * (func(start) + func(end))
        for i in range(1, n):
            integral += func(start + i * h)
        return integral * h


Task:
Translate the above Python code into C++, ensuring that all functionalities are preserved. Use the same class name (ParallelIntegrator) and method names (integrate, _worker). Ensure that all functionalities are preserved.
IMPORTANT: class name and testable function names MUST remain the same, only wrap code in a class if original code is wrapped in a class, other functions should also use snake_case.
IMPORTANT: All class MUST have getters and setters, and they should use get_ and set_ followed by attribute name respectively.
IMPORTANT: use the following function signatures in the C++ translated code:
double integrate(std::function<double(double)> func, double a, double b, int n = 1000);
static double _worker(std::function<double(double)> func, double start, double end, int n);
- IMPORTANT: Include all necessary headers required to execute the code.
- IMPORTANT: Include all bash commands for installing any dependencies necessary for compilation.
- IMPORTANT: code generated should be compatible with C++20 standard, and do NOT use deprecated syntax/library.
- IMPORTANT: Do not include main function because code will be tested against gtest framework.
- IMPORTANT: You MUST use C++ markdown for any C++ code generated.
- IMPORTANT: You MUST use bash markdown for any bash code generated.
- IMPORTANT: You MUST return C++ code in a single code block.
- IMPORTANT: You MUST use namepace std in the returned code ( `using namespace std;` )
- IMPORTANT: Do NOT wrap code in class if the original code/function signature is not wrapped in a class.
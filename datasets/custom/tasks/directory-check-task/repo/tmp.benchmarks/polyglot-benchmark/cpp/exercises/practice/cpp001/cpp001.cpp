
class ParallelIntegrator {

public:
    double integrate(std::function<double(double)> func, double a, double b, int n = 1000);

    static double _worker(std::function<double(double)> func, double start, double end, int n);
};
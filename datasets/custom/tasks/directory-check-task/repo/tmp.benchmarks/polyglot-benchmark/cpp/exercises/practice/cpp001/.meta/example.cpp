#include <vector>
#include <future>
#include <functional>
#include <stdexcept>
#include <thread>
#include <algorithm>

using namespace std;

class ParallelIntegrator {
private:
    int processes_;

public:
    ParallelIntegrator(int processes = 0) {
        if (processes < 1) {
            unsigned int hardwareProcs = std::thread::hardware_concurrency();
            processes_ = (hardwareProcs == 0 ? 1 : hardwareProcs);
        } else {
            processes_ = processes;
        }
    }

    int get_processes() const {
        return processes_;
    }

    void set_processes(int p) {
        if (p < 1) {
            unsigned int hardwareProcs = std::thread::hardware_concurrency();
            processes_ = (hardwareProcs == 0 ? 1 : hardwareProcs);
        } else {
            processes_ = p;
        }
    }

    double integrate(std::function<double(double)> func, double a, double b, int n = 1000) {
        if (a >= b) {
            throw std::invalid_argument("Invalid interval: a must be less than b");
        }

        int p = processes_;
        double range = b - a;
        int chunk_size = std::max(n / p, 1);

        vector<future<double>> futures;
        futures.reserve(p);

        for (int i = 0; i < p; ++i) {
            double start = a + i * (range / p);
            double end = a + (i + 1) * (range / p);
            futures.push_back(std::async(std::launch::async, [=]() {
                return _worker(func, start, end, chunk_size);
            }));
        }

        double result = 0.0;
        for (auto &f : futures) {
            result += f.get();
        }
        return result;
    }

    static double _worker(std::function<double(double)> func, double start, double end, int n) {
        double h = (end - start) / n;
        double integral = 0.5 * (func(start) + func(end));
        for (int i = 1; i < n; ++i) {
            integral += func(start + i * h);
        }
        return integral * h;
    }
};
#include <gtest/gtest.h>
#include <cmath>
#include <functional>
#include <stdexcept>

using namespace std;

class ParallelIntegratorTest : public ::testing::Test {
protected:
    ParallelIntegrator integrator;
};

// Test case for integrating a simple quadratic function
// This test checks if the integrator correctly computes the integral of x^2 from 0 to 1.
// The expected result is 1/3, and this test ensures the integrator handles basic polynomial functions correctly.
TEST_F(ParallelIntegratorTest, SimpleFunction) {
    auto func = [](double x) { return x * x; };
    double a = 0.0;
    double b = 1.0;
    double expected = 1.0 / 3.0;
    EXPECT_NEAR(integrator.integrate(func, a, b, 1000), expected, 1e-6);
}

// Test case for integrating a linear function
// This test checks if the integrator correctly computes the integral of x from 0 to 1.
// The expected result is 0.5, and this test ensures the integrator handles linear functions correctly.
TEST_F(ParallelIntegratorTest, LinearFunction) {
    auto func = [](double x) { return x; };
    double a = 0.0;
    double b = 1.0;
    double expected = 0.5;
    EXPECT_NEAR(integrator.integrate(func, a, b, 1000), expected, 1e-6);
}

// Test case for integrating a constant function
// This test checks if the integrator correctly computes the integral of a constant function from 0 to 1.
// The expected result is 1.0, and this test ensures the integrator handles constant functions correctly.
TEST_F(ParallelIntegratorTest, ConstantFunction) {
    auto func = [](double x) { return 1.0; };
    double a = 0.0;
    double b = 1.0;
    double expected = 1.0;
    EXPECT_NEAR(integrator.integrate(func, a, b, 1000), expected, 1e-6);
}

// Test case for integrating the cosine function
// This test checks if the integrator correctly computes the integral of cos(x) from 0 to π.
// The expected result is 0.0, and this test ensures the integrator handles trigonometric functions correctly.
TEST_F(ParallelIntegratorTest, CosineFunction) {
    auto func = [](double x) { return std::cos(x); };
    double a = 0.0;
    double b = M_PI;
    double expected = 0.0;
    EXPECT_NEAR(integrator.integrate(func, a, b, 1000), expected, 1e-6);
}

// Test case for integrating the exponential function
// This test checks if the integrator correctly computes the integral of exp(x) from 0 to 1.
// The expected result is exp(1) - 1, and this test ensures the integrator handles exponential functions correctly.
TEST_F(ParallelIntegratorTest, ExponentialFunction) {
    auto func = [](double x) { return std::exp(x); };
    double a = 0.0;
    double b = 1.0;
    double expected = std::exp(1.0) - 1.0;
    EXPECT_NEAR(integrator.integrate(func, a, b, 1000), expected, 1e-6);
}

// Test case for an invalid interval
// This test checks if the integrator correctly throws an exception for an invalid interval (a >= b).
// It ensures the integrator handles invalid input gracefully.
TEST_F(ParallelIntegratorTest, InvalidInterval) {
    auto func = [](double x) { return x; };
    double a = 1.0;
    double b = 0.0;
    EXPECT_THROW(integrator.integrate(func, a, b, 1000), std::invalid_argument);
}

// Test case for integrating a linear function over a large interval
// This test checks if the integrator correctly computes the integral of x from 0 to 1000.
// The expected result is 500000.0, and this test ensures the integrator handles large intervals correctly.
TEST_F(ParallelIntegratorTest, LargeInterval) {
    auto func = [](double x) { return x; };
    double a = 0.0;
    double b = 1000.0;
    double expected = 500000.0;
    EXPECT_NEAR(integrator.integrate(func, a, b, 1000), expected, 1e-6);
}

// Test case for integrating a zero function
// This test checks if the integrator correctly computes the integral of a zero function from 0 to 1.
// The expected result is 0.0, and this test ensures the integrator handles zero functions correctly.
TEST_F(ParallelIntegratorTest, ZeroFunction) {
    auto func = [](double x) { return 0.0; };
    double a = 0.0;
    double b = 1.0;
    double expected = 0.0;
    EXPECT_NEAR(integrator.integrate(func, a, b, 1000), expected, 1e-6);
}

// Performance test case for integrating a computationally intensive function
// This test checks if the integrator can compute the integral of sin(exp(x)) from 0 to 10
// with a large number of trapezoids within 120 seconds (120,000 ms).
// It ensures the parallel implementation is efficient for heavy workloads.
TEST_F(ParallelIntegratorTest, PerformanceTest) {
    auto func = [](double x) { return std::sin(std::exp(x)); };
    double a = 0.0;
    double b = 10.0;
    int n = 1000000; // Large number of trapezoids to stress performance
    auto t0 = testing::TimeInMillis();
    double result = integrator.integrate(func, a, b, n);
    auto t1 = testing::TimeInMillis();

    auto duration = t1 - t0;
    testing::Test::RecordProperty("execution_time_ms", duration);
    EXPECT_LT(duration, 120000) << "Integration took too long: " << duration << " ms";
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
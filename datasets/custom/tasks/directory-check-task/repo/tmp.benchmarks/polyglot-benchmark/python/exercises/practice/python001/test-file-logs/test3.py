import numpy as np

def pca(X: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    # On any invalid input, return two empty arrays
    if not isinstance(X, np.ndarray) or X.ndim != 2:
        return np.array([]), np.array([])
    if not isinstance(k, int):
        return np.array([]), np.array([])

    n_samples, n_features = X.shape
    if k < 1 or k > n_features or n_samples == 0:
        return np.array([]), np.array([])

    # Compute mean and center data
    X_mean = X.mean(axis=0)
    X_centered = X - X_mean

    # Covariance matrix (handle single-feature or single-sample)
    if n_samples == 1 or n_features == 1:
        cov = np.zeros((n_features, n_features))
    else:
        cov = (X_centered.T @ X_centered) / (n_samples - 1)

    # Eigen decomposition and sort
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvectors = eigenvectors[:, idx]

    # Project and reconstruct
    principal_components = eigenvectors[:, :k]
    X_proj = X_centered @ principal_components
    X_reconstruct = (X_proj @ principal_components.T) + X_mean

    return X_proj, X_reconstruct

### Performance test case to check the execution within 120 seconds
import unittest, time 
class TestPCAPerformance(unittest.TestCase):
    
    def test_performance_large_input_within_120_seconds(self):
        # Generate a large dataset: 100,000 samples, 100 features
        X = np.random.rand(100_000, 100)
        k = 20

        start_time = time.time()
        X_proj, X_reconstruct = pca(X, k)
        end_time = time.time()

        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time:.2f} seconds")

        self.assertLessEqual(
            elapsed_time, 120.0,
            msg=f"PCA execution exceeded time limit: {elapsed_time:.2f}s"
        )

        self.assertEqual(X_proj.shape, (100_000, k))
        self.assertEqual(X_reconstruct.shape, (100_000, 100))

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)

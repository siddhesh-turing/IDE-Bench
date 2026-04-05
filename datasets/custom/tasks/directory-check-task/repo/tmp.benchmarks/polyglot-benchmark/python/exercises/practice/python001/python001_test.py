from solution import pca

import unittest , time
import numpy as np
class TestPCA(unittest.TestCase):

    # Happy Cases
    def test_HC_basic_pca(self):
        X = np.array([[1, 2], [2, 2], [3, 3], [4, 4]])
        k = 1
        X_proj, X_reconstruct = pca(X, k)
        self.assertIsInstance(X_proj, np.ndarray)
        self.assertIsInstance(X_reconstruct, np.ndarray)
        self.assertEqual(X_proj.shape, (4, 1))
        self.assertEqual(X_reconstruct.shape, (4, 2))
    
    def test_HC_centering(self):
        X = np.array([[1, 2], [2, 3], [3, 4]])
        X_mean = np.mean(X, axis=0)
        X_centered = X - X_mean
        X_proj, X_reconstruct = pca(X, 1)
        X_centered_from_pca = X_reconstruct - np.mean(X_reconstruct, axis=0)
        np.testing.assert_allclose(np.mean(X_centered_from_pca, axis=0), np.array([0.0, 0.0]), atol=1e-9)

    def test_HC_covariance_calculation(self):
        X = np.array([[1, 2], [2, 3], [3, 4]])
        expected_cov = np.cov(X, rowvar=False)
        X_proj, X_reconstruct = pca(X, 1)
        X_centered = X - np.mean(X, axis=0)
        cov_matrix_from_pca = np.cov(X_centered, rowvar=False)
        np.testing.assert_allclose(cov_matrix_from_pca, expected_cov, atol=1e-9)

    def test_HC_projection_and_reconstruction(self):
        X = np.array([[1, 2], [2, 2], [3, 3]])
        k = 1
        X_proj, X_reconstruct = pca(X, k)
        total_variance = np.sum(np.var(X, axis=0))
        reconstruction_error = np.mean((X - X_reconstruct)**2)
        relative_error = reconstruction_error / total_variance
        self.assertLess(relative_error, 0.05)

    def test_HC_single_sample(self):
        X = np.array([[1, 2]])
        k = 1
        X_proj, X_reconstruct = pca(X, k)
        self.assertIsInstance(X_proj, np.ndarray)
        self.assertIsInstance(X_reconstruct, np.ndarray)

    def test_HC_single_feature(self):
        X = np.array([[1], [2], [3]])
        k = 1
        X_proj, X_reconstruct = pca(X, k)
        self.assertIsInstance(X_proj, np.ndarray)
        self.assertIsInstance(X_reconstruct, np.ndarray)

    def test_HC_k_equals_n_features(self):
        X = np.array([[1, 2], [2, 2], [3, 3]])
        k = 2
        X_proj, X_reconstruct = pca(X, k)
        self.assertIsInstance(X_proj, np.ndarray)
        self.assertIsInstance(X_reconstruct, np.ndarray)
        self.assertEqual(X_proj.shape, (3, 2))
        self.assertEqual(X_reconstruct.shape, (3, 2))

    def test_HC_identical_samples(self):
        X = np.array([[1, 2], [1, 2], [1, 2]])
        k = 1
        X_proj, X_reconstruct = pca(X, k)
        self.assertIsInstance(X_proj, np.ndarray)
        self.assertIsInstance(X_reconstruct, np.ndarray)
        self.assertEqual(X_proj.shape, (3, 1))
        self.assertEqual(X_reconstruct.shape, (3, 2))

    # Edge Cases
    def test_EC_eigenvalue_sorting(self):
        X = np.array([[1, 2], [2, 2], [3, 3]])
        k = 1
        X_proj, X_reconstruct = pca(X, k)
        eigenvalues, _ = np.linalg.eig(np.cov(X - np.mean(X, axis=0), rowvar=False))
        sorted_eigenvalues = sorted(eigenvalues, reverse=True)
        self.assertTrue(np.all(eigenvalues == sorted_eigenvalues))

    def test_EC_invalid_input_X_type(self):
        X = [[1, 2], [2, 2]]
        k = 1
        X_proj, X_reconstruct = pca(X, k)
        self.assertEqual(X_proj.size, 0)
        self.assertEqual(X_reconstruct.size, 0)

    def test_EC_invalid_input_X_ndim(self):
        X = np.array([1, 2, 3])
        k = 1
        X_proj, X_reconstruct = pca(X, k)
        self.assertEqual(X_proj.size, 0)
        self.assertEqual(X_reconstruct.size, 0)

    def test_EC_invalid_input_k_type(self):
        X = np.array([[1, 2], [2, 2]])
        k = "1"
        X_proj, X_reconstruct = pca(X, k)
        self.assertEqual(X_proj.size, 0)
        self.assertEqual(X_reconstruct.size, 0)

    def test_EC_invalid_input_k_value(self):
        X = np.array([[1, 2], [2, 2]])
        k = 3
        X_proj, X_reconstruct = pca(X, k)
        self.assertEqual(X_proj.size, 0)
        self.assertEqual(X_reconstruct.size, 0)

    def test_EC_empty_data(self):
        X = np.array([])
        k = 1
        X_proj, X_reconstruct = pca(X, k)
        self.assertEqual(X_proj.size, 0)
        self.assertEqual(X_reconstruct.size, 0)

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

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
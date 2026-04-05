@testable import swift001
import XCTest
final class MaximumArrayXOR__TestCases: XCTestCase {
    var response = MaximumArrayXOR()
    /// Analyzes a given integer array to compute various algorithmic insights.
    /// This method performs the following evaluations:
    /// - Computes the maximum XOR value of any subarray.
    /// - Finds the length of the longest subarray with sum equal to zero.
    /// - Determines the k-th smallest element (1-indexed) using QuickSelect.
    /// - Calculates the product of all elements except the current index, without using division.
    /// - Identifies the majority element (appearing more than ⌊n/2⌋ times) using the Boyer–Moore voting algorithm.
    /// - Parameters:
    ///   - nums: The input array of integers to analyze.
    ///   - k: The 1-based index for the k-th smallest element.
    /// - Returns: A `ResultAnalysis` struct containing all computed metrics.
    override func setUp() {
        super.setUp()
    }
    // Happy Case
    func test_HC_ProductExceptSelf() {
        let nums = [1, 2, 3, 4]
        XCTAssertEqual(response.analyzeArrayFeatures(nums: nums, k: 2).productExceptSelf, [24, 12, 8, 6])
    }
    // Happy Case
    func test_HC_MajorityElementExists() {
        let nums = [2, 2, 1, 1, 2, 2, 2]
        XCTAssertEqual(response.analyzeArrayFeatures(nums: nums, k: 3).majorityElement, 2)
    }
    // Happy Case
    func test_HC_KthSmallestBasicCase() {
        let nums = [3, 2, 1, 5, 6, 4]
        let result = response.analyzeArrayFeatures(nums: nums, k: 2)
        XCTAssertEqual(result.kthSmallest, 2)
    }
    // Edge Case
    func test_EC_KthSmallestWithNegativeNumbers() {
        let nums = [-5, -10, -3, -7, -1]
        XCTAssertEqual(response.analyzeArrayFeatures(nums: nums, k: 3).kthSmallest, -5)
    }
    // Happy Case
    func test_HC_NoMajorityElement() {
        let nums = [1, 2, 3, 4, 5]
        XCTAssertNil(response.analyzeArrayFeatures(nums: nums, k: 1).majorityElement)
    }
    // Edge Case
    func test_EC_EmptyArray() {
        let nums: [Int] = []
        let result = response.analyzeArrayFeatures(nums: nums, k: 1)
        XCTAssertEqual(result.maxXOR, 0)
        XCTAssertEqual(result.longestZeroSumSubarray, 0)
        XCTAssertEqual(result.kthSmallest, -1)
        XCTAssertEqual(result.productExceptSelf, [])
        XCTAssertNil(result.majorityElement)
    }
    // Edge Case
    func test_EC_KthSmallestOutOfBounds() {
        let nums = [10, 20, 30]
        XCTAssertEqual(response.analyzeArrayFeatures(nums: nums, k: 10).kthSmallest, -1)
    }
    // Edge Case
    func test_EC_AllZeros() {
        let nums = [0, 0, 0, 0]
        XCTAssertEqual(response.analyzeArrayFeatures(nums: nums, k: 1).longestZeroSumSubarray, 4)
    }
    // Edge Case
    func test_EC_LargeNumbers() {
        let nums = [10000, -10000, -100, 50, 100]
        let result = response.analyzeArrayFeatures(nums: nums, k: 3)
        XCTAssertEqual(result.kthSmallest, 50)
    }
    // Edge Case
    func test_EC_NegativeAndPositiveMix() {
        let nums = [-1, -2, 3, 1, 2, -3]
        XCTAssertEqual(response.analyzeArrayFeatures(nums: nums, k: 4).kthSmallest, 1)
    }
    // Happy Case
    func test_HC_SingleElement() {
        let nums = [42]
        XCTAssertEqual(response.analyzeArrayFeatures(nums: nums, k: 1).kthSmallest, 42)
    }
    // Happy Case
    func test_HC_AllSameElements() {
        let nums = [5, 5, 5, 5, 5]
        XCTAssertEqual(response.analyzeArrayFeatures(nums: nums, k: 3).kthSmallest, 5)
    }
    // Happy Case
    func test_HC_MaxXOR() {
        let nums = [8, 1, 2, 12, 7, 6]
        XCTAssertEqual(response.analyzeArrayFeatures(nums: nums, k: 3).maxXOR, 15)
    }
    // Edge Case
    func test_EC_LongestZeroSumSubarray() {
        let nums = [1, 2, -3, 3, 1]
        XCTAssertEqual(response.analyzeArrayFeatures(nums: nums, k: 1).longestZeroSumSubarray, 3)
    }
    
    /// Performance Test - Should complete within 120 seconds
    func test_EC_Performance() {
        let timeoutLimit: TimeInterval = 120.0
        
        // large input for realistic stress testing while avoiding arithmetic overflow
        // Negative numbers help reduce product magnitude when multiplied
        var largeArray: [Int] = []
        for i in 0..<5000000 {
            let value = (i % 6) - 2  // Range: -2, -1, 0, 1, 2, 3
            largeArray.append(value)
        }
        let k = 25000000
        
        let startTime = Date()
        _ = response.analyzeArrayFeatures(nums: largeArray, k: k)
        let elapsed = Date().timeIntervalSince(startTime)
        print("Execution took \(elapsed) seconds")
        XCTAssertLessThanOrEqual(elapsed, timeoutLimit, "Execution exceeded \(timeoutLimit) seconds.")
    }
}
extension MaximumArrayXOR__TestCases {
    static var allTests = [
        ("test_HC_ProductExceptSelf", test_HC_ProductExceptSelf),
        ("test_HC_MajorityElementExists", test_HC_MajorityElementExists),
        ("test_HC_KthSmallestBasicCase", test_HC_KthSmallestBasicCase),
        ("test_EC_KthSmallestWithNegativeNumbers", test_EC_KthSmallestWithNegativeNumbers),
        ("test_HC_NoMajorityElement", test_HC_NoMajorityElement),
        ("test_EC_EmptyArray", test_EC_EmptyArray),
        ("test_EC_KthSmallestOutOfBounds", test_EC_KthSmallestOutOfBounds),
        ("test_EC_AllZeros", test_EC_AllZeros),
        ("test_EC_LargeNumbers", test_EC_LargeNumbers),
        ("test_EC_NegativeAndPositiveMix", test_EC_NegativeAndPositiveMix),
        ("test_HC_SingleElement", test_HC_SingleElement),
        ("test_HC_AllSameElements", test_HC_AllSameElements),
        ("test_HC_MaxXOR", test_HC_MaxXOR),
        ("test_EC_LongestZeroSumSubarray", test_EC_LongestZeroSumSubarray),
        ("test_EC_Performance", test_EC_Performance)
    ]
}

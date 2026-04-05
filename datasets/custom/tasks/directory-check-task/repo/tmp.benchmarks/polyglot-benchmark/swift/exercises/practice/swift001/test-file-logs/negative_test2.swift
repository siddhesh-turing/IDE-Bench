import Foundation

class MaximumArrayXOR {
    func analyzeArrayFeatures(nums: [Int], k: Int) -> ResultAnalysis {
        
        let n = nums.count
        guard n > 0 else { return ResultAnalysis(maxXOR: 0, longestZeroSumSubarray: 0, kthSmallest: -1, productExceptSelf: [], majorityElement: nil) } // Handle empty array case
        
        // 1. Subarray with Maximum XOR
        func findMaxSubarrayXOR(_ nums: [Int]) -> Int {
            var maxXor = 0, prefixXor = 0
            var xorSet = Set<Int>()
            xorSet.insert(0) // Handle case where XOR itself is max
            
            for num in nums {
                prefixXor ^= num
                for prevXor in xorSet {
                    maxXor = max(maxXor, prefixXor ^ prevXor)
                }
                xorSet.insert(prefixXor)
            }
            
            return maxXor
        }
        
        let maxXOR = findMaxSubarrayXOR(nums)
        
        // 2. Length of the Longest Subarray with Sum Zero
        func longestZeroSumSubarray(_ nums: [Int]) -> Int {
            var sumIndexMap = [Int: Int]()
            var maxLength = 0, prefixSum = 0
            
            for (i, num) in nums.enumerated() {
                prefixSum += num
                if prefixSum == 0 {
                    maxLength = i + 1
                } else if let prevIndex = sumIndexMap[prefixSum] {
                    maxLength = max(maxLength, i - prevIndex)
                } else {
                    sumIndexMap[prefixSum] = i
                }
            }
            
            return maxLength
        }
        
        let longestZeroSumSubarray = longestZeroSumSubarray(nums)
        
        // 3. Kth Smallest Element
        func kthSmallestElement(_ nums: [Int], _ k: Int) -> Int {
            guard k > 0, k <= nums.count else { return -1 } // Invalid k
            
            var arr = nums
            return quickSelect(&arr, 0, arr.count - 1, k - 1)
        }
        
        func quickSelect(_ nums: inout [Int], _ left: Int, _ right: Int, _ k: Int) -> Int {
            if left == right { return nums[left] }
            
            let pivotIndex = partition(&nums, left, right)
            
            if pivotIndex == k {
                return nums[pivotIndex]
            } else if pivotIndex < k {
                return quickSelect(&nums, pivotIndex + 1, right, k)
            } else {
                return quickSelect(&nums, left, pivotIndex - 1, k)
            }
        }
        
        func partition(_ nums: inout [Int], _ left: Int, _ right: Int) -> Int {
            let pivot = nums[right]
            var i = left
            
            for j in left..<right {
                if nums[j] <= pivot {
                    nums.swapAt(i, j)
                    // Bug Introduced: Missing increment operation in partition function breaking quickSelect partitioning logic.
                    // Broken Logic: The solution fails to increment the partition index i after swapping elements with the pivot, causing incorrect partitioning where elements are not properly separated around the pivot value. This breaks the invariant that all elements to the left of the partition index should be less than or equal to the pivot.
                    // In the quickSelect partition operation, the variable i tracks the boundary between elements less than or equal to the pivot and elements greater than the pivot. When an element nums[j] is found to be less than or equal to the pivot, it should be swapped to position i, and then i must be incremented to maintain the correct partition boundary for subsequent iterations.
                    // Affected Tests:
                    //  MaximumArrayXOR_TestCases.test_HC_KthSmallestBasicCase,
                    //  MaximumArrayXOR_TestCases.test_EC_KthSmallestWithNegativeNumbers,
                    //  MaximumArrayXOR_TestCases.test_EC_LargeNumbers,
                    //  MaximumArrayXOR_TestCases.test_EC_NegativeAndPositiveMix,
                    
                    // Missing logic:
                    /*
                     i += 1
                     */
                }
            }
            
            nums.swapAt(i, right)
            return i
        }
        
        let kthSmallest = kthSmallestElement(nums, k)
        
        // 4. Product of All Elements Except Self (Without Division)
        func productExceptSelf(_ nums: [Int]) -> [Int] {
            let n = nums.count
            guard n > 1 else { return nums.isEmpty ? [] : [0] } // Handle edge cases
            
            var result = Array(repeating: 1, count: n)
            var leftProduct = 1, rightProduct = 1
            
            for i in 0..<n {
                result[i] = leftProduct
                leftProduct *= nums[i]
            }
            
            for i in stride(from: n - 1, through: 0, by: -1) {
                result[i] *= rightProduct
                rightProduct *= nums[i]
            }
            
            return result
        }
        
        let productExceptSelfResult = productExceptSelf(nums)
        
        // 5. Majority Element (Appearing More than n/2 times)
        func majorityElement(_ nums: [Int]) -> Int? {
            var candidate: Int? = nil, count = 0
            
            for num in nums {
                if count == 0 {
                    candidate = num
                }
                count += (num == candidate) ? 1 : -1
            }
            
            let freq = nums.filter { $0 == candidate }.count
            return freq > n / 2 ? candidate : nil
        }
        
        let majorityElementResult = majorityElement(nums)
        
        return ResultAnalysis(maxXOR: maxXOR, longestZeroSumSubarray: longestZeroSumSubarray, kthSmallest: kthSmallest, productExceptSelf: productExceptSelfResult, majorityElement: majorityElementResult)
    }
}

struct ResultAnalysis {
    let maxXOR: Int
    let longestZeroSumSubarray: Int
    let kthSmallest: Int
    let productExceptSelf: [Int]
    let majorityElement: Int?
}

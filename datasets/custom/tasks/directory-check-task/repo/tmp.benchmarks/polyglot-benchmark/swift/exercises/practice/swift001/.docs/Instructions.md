YOU ARE GIVEN:
- A CODING PROBLEM
- A TARGET LANGUAGE: `Swift`

YOUR OBJECTIVE:
WRITE A COMPLETE, EXECUTABLE, AND SELF-CONTAINED SOLUTION IN SWIFT THAT FULFILLS THE FOLLOWING CRITERIA:

### REQUIRED STRUCTURE:

1. CLASS-WRAPPED IMPLEMENTATION:
   - Your solution MUST be inside a class
   - Use the exact class name and method signature given in the prompt
   - Your solution must use instance methods only
   - DO NOT use static methods
   - DO NOT add initializers (`init`) in the class

2. SELF-CONTAINED LOGIC:
   - Include all necessary functions, classes, and helper logic inside the same code block

3. NECESSARY IMPORTS:
   * Must include imports for Apple Built-in Frameworks whenever a response snippet relies on components from them -
     Examples: `Foundation`, `SwiftUI`, `UIKit`, `Combine`, `CoreData`, `MapKit`, etc.
   * If the code uses classes, structs, or functions from a framework, import that framework explicitly.
   * Avoid importing external libraries or packages unless the user explicitly requests their usage.

4. OPTIMIZATION:
   - Your implementation MUST be optimized to complete all test cases within 120 seconds.

### WHAT NOT TO INCLUDE:
- DO NOT include `main()` or driver code
- DO NOT include usage examples or comments
- DO NOT include test cases (e.g., `XCTest`, `SwiftTests`)
- DO NOT use `print()` statements or any debugging output
- DO NOT return only a function — IT MUST BE INSIDE A CLASS

### EXTERNAL LIBRARIES:
- If external libraries are REQUIRED:
  - Provide a separate code block at the top with the installation commands (e.g., using Swift Package Manager)
  - Then, include the main solution as a second code block (still following all rules)

---

# Problem Statement:
Consider the Kotlin code below. I need to migrate it to Swift language.  Use the same class and function names, and avoid using underscores 
for the parameters.
The algorithm should do the following:
- Max Subarray XOR: Identify the maximum XOR value obtainable from any contiguous subarray in nums. For invalid or empty input, return 0
- Longest Subarray with Sum Zero: Determine the length of the longest contiguous subarray whose sum is exactly zero. For invalid or empty input, return 0
- K-th Smallest Element: Compute the k-th smallest element in the array (1-indexed). Assume 1 ≤ k ≤ nums.count. If k is less than 1 or greater than the number of elements in nums, the function must return -1 as the fallback value for the k-th smallest element, indicating an invalid query.
- Product of All Elements Except Self: Construct an array such that each element at index i is the product of all elements in nums except nums[i], without using division. For invalid or empty input, return []
- Majority Element (Boyer–Moore): Return the majority element (if any) that appears more than ⌊n/2⌋ times using the Boyer–Moore majority vote algorithm. For invalid or empty input, return nil
- Check that code and ensure it fits the above contraints and edge cases including empty values are well handled.


```kotlin
class MaximumArrayXOR {
    override fun analyzeArrayFeatures(nums: List<Int>, k: Int): ResultAnalysis {
        // 1. Subarray with Maximum XOR
        fun maxSubarrayXOR(nums: List<Int>): Int {
            var maxXOR = 0
            var prefixXOR = 0
            val prefixSet = mutableSetOf(0)

            for (num in nums) {
                prefixXOR = prefixXOR xor num
                for (p in prefixSet) {
                    maxXOR = maxOf(maxXOR, prefixXOR xor p)
                }
                prefixSet.add(prefixXOR)
            }
            return maxXOR
        }

        // 2. Length of the Longest Subarray with Sum Zero
        fun longestZeroSumSubarray(nums: List<Int>): Int {
            var sum = 0
            var maxLength = 0
            val sumIndexMap = mutableMapOf(0 to -1)

            for ((i, num) in nums.withIndex()) {
                sum += num
                if (sumIndexMap.containsKey(sum)) {
                    maxLength = maxOf(maxLength, i - sumIndexMap[sum]!!)
                } else {
                    sumIndexMap[sum] = i
                }
            }
            return maxLength
        }

        // 3. Kth Smallest Element in the Array
        fun kthSmallest(nums: List<Int>, k: Int): Int {
            fun quickSelect(nums: MutableList<Int>, left: Int, right: Int, k: Int): Int {
                val pivot = nums[right]
                var pIndex = left
                for (i in left until right) {
                    if (nums[i] <= pivot) {
                        nums[i] = nums[pIndex].also { nums[pIndex] = nums[i] }
                        pIndex++
                    }
                }
                nums[right] = nums[pIndex].also { nums[pIndex] = nums[right] }

                return when {
                    pIndex == k -> nums[pIndex]
                    pIndex < k -> quickSelect(nums, pIndex + 1, right, k)
                    else -> quickSelect(nums, left, pIndex - 1, k)
                }
            }

            val numsCopy = nums.toMutableList()
            return quickSelect(numsCopy, 0, numsCopy.size - 1, k - 1)
        }

        // 4. Product of All Elements Except Self
        fun productExceptSelf(nums: List<Int>): List<Int> {
            val n = nums.size
            val result = MutableList(n) { 1 }

            var leftProduct = 1
            for (i in nums.indices) {
                result[i] = leftProduct
                leftProduct *= nums[i]
            }

            var rightProduct = 1
            for (i in nums.indices.reversed()) {
                result[i] *= rightProduct
                rightProduct *= nums[i]
            }

            return result
        }

        // 5. Find the Majority Element
        fun findMajorityElement(nums: List<Int>): Int? {
            var candidate: Int? = null
            var count = 0

            for (num in nums) {
                if (count == 0) {
                    candidate = num
                }
                count += if (num == candidate) 1 else -1
            }

            // Verify the candidate
            return candidate?.takeIf { num -> nums.count { it == num } > nums.size / 2 }
        }

        return ResultAnalysis(
            maxXOR = maxSubarrayXOR(nums),
            longestZeroSumSubarray = longestZeroSumSubarray(nums),
            kthSmallest = kthSmallest(nums, k),
            productExceptSelf = productExceptSelf(nums),
            majorityElement = findMajorityElement(nums)
        )
    }
}

data class ResultAnalysis(
    val maxXOR: Int,
    val longestZeroSumSubarray: Int,
    val kthSmallest: Int,
    val productExceptSelf: List<Int>,
    val majorityElement: Int?
)
```

### OUTPUT FORMAT:
- Output your final implementation inside a SINGLE markdown code block
- Format your code using proper Swift syntax highlighting:
  - Class Name: MaximumArrayXOR
  - Method Signature
  ```swift
  func analyzeArrayFeatures(nums: [Int], k: Int) -> ResultAnalysis
  ```
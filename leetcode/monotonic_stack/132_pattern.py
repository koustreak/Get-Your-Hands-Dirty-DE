"""
LeetCode 456: 132 Pattern
==========================

সমস্যা বিবরণ (Problem Statement in Bengali):
--------------------------------------------
একটি integer array `nums` দেওয়া আছে। একটি **132 pattern** হলো তিনটি integer 
`nums[i]`, `nums[j]`, `nums[k]` এর একটি subsequence যাতে:
- i < j < k (index অর্ডার maintain করতে হবে)
- nums[i] < nums[k] < nums[j] (value অর্ডার: 1 < 3 < 2 pattern)

Array-এ 132 pattern আছে কিনা চেক করুন। থাকলে `true`, নাইলে `false` রিটার্ন করুন।

Example 1:
Input: nums = [1,2,3,4]
Output: false
ব্যাখ্যা: কোনো 132 pattern নেই।

Example 2:
Input: nums = [3,1,4,2]
Output: true
ব্যাখ্যা: 132 pattern আছে: [1, 4, 2] (i=1, j=2, k=3)

Example 3:
Input: nums = [-1,3,2,0]
Output: true
ব্যাখ্যা: তিনটি 132 pattern আছে: [-1, 3, 2], [-1, 3, 0], [-1, 2, 0]

Constraints:
- n == nums.length
- 1 <= n <= 2 * 10^5
- -10^9 <= nums[i] <= 10^9

সমাধান পদ্ধতি (Solution Approach):
-----------------------------------
এটি একটি **Monotonic Stack** problem (Right to Left traversal):
1. ডান থেকে বামে (right to left) traverse করুন
2. `max_k` variable রাখুন যা `nums[k]`-এর maximum possible value track করবে (initially -inf)
3. Stack-এ `nums[j]` candidates রাখব (monotonic decreasing stack)
4. প্রতিটি `nums[i]` (current element) এর জন্য:
   - যদি `nums[i] < max_k`: 132 pattern পাওয়া গেলো! Return true
   - Stack খালি না হলে এবং `nums[i] > stack[-1]`: 
     - Stack top pop করুন এবং `max_k` আপডেট করুন (এটি potential `nums[k]`)
   - `nums[i]` stack-এ push করুন (potential `nums[j]`)
5. Loop শেষে pattern না পেলে false রিটার্ন করুন

Key Insight: Stack maintains decreasing sequence of potential `nums[j]` values.
When we find a larger `nums[i]`, we pop smaller values which become candidates for `nums[k]`.

Time Complexity: O(n), Space Complexity: O(n)
"""

from typing import List


class Solution:
    def find132pattern(self, nums: List[int]) -> bool:
        """
        Array-এ 132 pattern আছে কিনা চেক করুন।
        
        Args:
            nums: List of integers
            
        Returns:
            True if 132 pattern exists, False otherwise
        """
        stack = []

        max_k = float('-inf')

        for i in range(len(nums) - 1, -1, -1):
            if nums[i]<max_k:
                return True
            while stack and nums[i]>stack[-1]:
                max_k = stack.pop()
            
            stack.append(nums[i])
        
        return False


# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (nums, expected_output, description)
        (
            [1, 2, 3, 4],
            False,
            "Example 1: Strictly increasing - no pattern"
        ),
        (
            [3, 1, 4, 2],
            True,
            "Example 2: Basic 132 pattern [1,4,2]"
        ),
        (
            [-1, 3, 2, 0],
            True,
            "Example 3: Multiple patterns with negative"
        ),
        (
            [1, 0, 1, -4, -3],
            False,
            "Edge case: Decreasing then increasing"
        ),
        (
            [1, 2, 3, 4, 5],
            False,
            "Edge case: Strictly increasing"
        ),
        (
            [5, 4, 3, 2, 1],
            False,
            "Edge case: Strictly decreasing"
        ),
        (
            [3, 5, 0, 3, 4],
            True,
            "Edge case: Pattern with duplicate 3s"
        ),
        (
            [1, 3, 2],
            True,
            "Edge case: Minimum length 3 with pattern"
        ),
        (
            [1, 2, 3],
            False,
            "Edge case: Minimum length 3 without pattern"
        ),
        (
            [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            False,
            "Edge case: Long decreasing sequence"
        ),
        (
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            False,
            "Edge case: Long increasing sequence"
        ),
        (
            [-2, 1, 2, -2, 1, 2],
            False,
            "Edge case: Repeating pattern without 132"
        ),
        (
            [1, 4, 0, -1, -2, -3, -1, -2],
            True,
            "Edge case: Pattern with negatives"
        ),
        (
            [8, 10, 4, 6, 5],
            True,
            "Edge case: Pattern [4,6,5]"
        ),
        (
            [1, 0, 1, -4, -3],
            False,
            "Edge case: No valid k for any j"
        ),
    ]
    
    print("=" * 70)
    print("Running Tests for 132 Pattern (LeetCode 456)")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for i, (nums, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.find132pattern(nums)
            if result == expected:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    Input:    {nums}")
                print(f"    Output:   {result}")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    Input:    {nums}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    Input:    {nums}")
            print(f"    Exception: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    run_tests()
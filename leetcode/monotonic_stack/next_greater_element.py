"""
LeetCode 496: Next Greater Element I
=====================================

সমস্যা বিবরণ (Problem Statement in Bengali):
-------------------------------------------
দুটি distinct 0-indexed integer array দেওয়া আছে: nums1 এবং nums2।
nums1, nums2-এর একটি subset (উপসেট)।

প্রতিটি element x এর জন্য nums1-এ, আমাদের nums2-এ x-এর "next greater element" খুঁজে বের করতে হবে।
Next greater element বলতে nums2-এ x-এর ডানে (right side) থাকা প্রথম (first) বড় element কে বোঝায়।
যদি কোনো বড় element না থাকে, তবে answer হবে -1।

প্রতিটি 0 <= i < nums1.length এর জন্য:
- nums2-এ index j খুঁজুন যাতে nums1[i] == nums2[j]
- nums2[j]-এর next greater element nums2-এ নির্ণয় করুন
- না পেলে -1 দিন

Output: ans array of length nums1.length, যেখানে ans[i] = next greater element

Example 1:
Input: nums1 = [4,1,2], nums2 = [1,3,4,2]
Output: [-1,3,-1]
ব্যাখ্যা:
- 4 nums2-এ [1,3,4,2]-এ আছে। এর ডানে কোনো বড় element নেই → -1
- 1 nums2-এ আছে। এর ডানে 3 আছে (first greater) → 3
- 2 nums2-এ আছে। এর ডানে কোনো বড় element নেই → -1

Example 2:
Input: nums1 = [2,4], nums2 = [1,2,3,4]
Output: [3,-1]
ব্যাখ্যা:
- 2-এর next greater = 3
- 4-এর next greater = -1 (কোনো বড় element নেই)

Constraints:
- 1 <= nums1.length <= nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 10^4
- nums1 এবং nums2-এ সব integer unique
- nums1-এর সব integer nums2-এও আছে

Follow-up: O(nums1.length + nums2.length) solution খুঁজুন
Hint: Monotonic Stack ব্যবহার করুন
"""

from typing import List


class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """
        nums1-এর প্রতিটি element-এর জন্য nums2-এ next greater element খুঁজে বের করুন।
        
        Args:
            nums1: Query array (subset of nums2)
            nums2: Main array where we search for next greater elements
            
        Returns:
            List of next greater elements for each element in nums1
        """
        
        greater_map = dict()
        stack = []

        for num in nums2:
            while stack and stack[-1]<num:
                prev_num = stack.pop()
                greater_map[prev_num] = num 

            stack.append(num)

        print(greater_map)

        while stack:
            prev_num = stack.pop()
            greater_map [prev_num] = -1

        return [greater_map[num] for num in nums1]
                

# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (nums1, nums2, expected_output, description)
        (
            [4, 1, 2],
            [1, 3, 4, 2],
            [-1, 3, -1],
            "Example 1: Basic case"
        ),
        (
            [2, 4],
            [1, 2, 3, 4],
            [3, -1],
            "Example 2: Increasing sequence"
        ),
        (
            [1],
            [1],
            [-1],
            "Edge case: Single element"
        ),
        (
            [1, 3, 5],
            [1, 2, 3, 4, 5],
            [2, 4, -1],
            "Edge case: All elements have next greater except last"
        ),
        (
            [5, 4, 3, 2, 1],
            [5, 4, 3, 2, 1],
            [-1, -1, -1, -1, -1],
            "Edge case: Strictly decreasing - no next greater for any"
        ),
        (
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [2, 3, 4, 5, -1],
            "Edge case: Strictly increasing - all have next greater except last"
        ),
        (
            [2, 1, 3],
            [2, 3, 1],
            [3, 3, -1],
            "Edge case: nums2 not sorted"
        ),
        (
            [1, 2],
            [2, 1],
            [-1, -1],
            "Edge case: nums2 reverse order"
        ),
        (
            [3, 1, 2],
            [1, 3, 2, 4],
            [4, 3, 4],
            "Edge case: Multiple elements with same next greater"
        ),
        (
            [10, 20, 30],
            [10, 20, 30, 40, 50],
            [20, 30, 40],
            "Edge case: Larger numbers"
        ),
    ]
    
    print("=" * 60)
    print("Running Tests for Next Greater Element I (LeetCode 496)")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for i, (nums1, nums2, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.nextGreaterElement(nums1, nums2)
            if result == expected:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    nums1 = {nums1}")
                print(f"    nums2 = {nums2}")
                print(f"    Output: {result}")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    nums1 = {nums1}")
                print(f"    nums2 = {nums2}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    nums1 = {nums1}")
            print(f"    nums2 = {nums2}")
            print(f"    Exception: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    run_tests()
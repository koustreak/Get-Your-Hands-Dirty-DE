"""
LeetCode 402: Remove K Digits
==============================

সমস্যা বিবরণ (Problem Statement in Bengali):
--------------------------------------------
একটি string `num` দেওয়া আছে যা একটি non-negative integer রিপ্রেজেন্ট করে, 
এবং একটি integer `k` দেওয়া আছে। `num`- থেকে `k` টি ডিজিট রিমুভ করে 
সবচেয়ে ছোট সম্ভাব্য integer বানাতে হবে।

Example 1:
Input: num = "1432219", k = 3
Output: "1219"
ব্যাখ্যা: 4, 3, এবং 2 রিমুভ করলে 1219 পাওয়া যায় যা সবচেয়ে ছোট।

Example 2:
Input: num = "10200", k = 1
Output: "200"
ব্যাখ্যা: শুরুর 1 রিমুভ করলে 200 পাওয়া যায়। Leading zeroes থাকতে পারবে না।

Example 3:
Input: num = "10", k = 2
Output: "0"
ব্যাখ্যা: সব ডিজিট রিমুভ করলে 0 থাকে।

Constraints:
- 1 <= k <= num.length <= 10^5
- num শুধু ডিজিট দিয়ে গঠিত
- num-এ leading zeros নেই (শুধু "0" ছাড়া)

সমাধান পদ্ধতি (Solution Approach):
-----------------------------------
এটি একটি classic **Monotonic Stack** problem:
1. Stack ব্যবহার করুন (monotonic increasing order maintain করব)
2. প্রতিটি ডিজিটের জন্য:
   - যতক্ষণ k > 0 এবং stack খালি নয় এবং current digit < stack top:
     - Stack top pop করুন, k-- করুন
   - Current digit stack-এ push করুন
3. Loop শেষে যদি k > 0 থাকে, stack-এর শেষ থেকে k টি pop করুন
4. Stack কে join করুন, leading zeros trim করুন
5. যদি ফলাফল খালি হয়, "0" রিটার্ন করুন

Time Complexity: O(n), Space Complexity: O(n)
"""

from typing import List


class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        """
        k টি ডিজিট রিমুভ করে সবচেয়ে ছোট সম্ভাব্য সংখ্যা রিটার্ন করুন।
        
        Args:
            num: String representing a non-negative integer
            k: Number of digits to remove
            
        Returns:
            Smallest possible integer as string after removing k digits
        """
        stack = []

        for digit in num:
            while k > 0 and stack and stack[-1] > digit:
                stack.pop()
                k -= 1
            stack.append(digit)

        # যদি k এখনও > 0 থাকে, stack-এর শেষ থেকে k টি pop করুন
        if k>0:
            stack = stack[:-k]

        # Stack কে join করুন এবং leading zeros trim করুন
        result = ''.join(stack).lstrip('0')

        # যদি ফলাফল খালি হয়, "0" রিটার্ন করুন
        return result if result else "0"


# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (num, k, expected_output, description)
        (
            "1432219", 3,
            "1219",
            "Example 1: Basic case"
        ),
        (
            "10200", 1,
            "200",
            "Example 2: Leading zero handling"
        ),
        (
            "10", 2,
            "0",
            "Example 3: Remove all digits"
        ),
        (
            "112", 1,
            "11",
            "Edge case: Duplicate digits"
        ),
        (
            "12345", 2,
            "123",
            "Edge case: Strictly increasing - remove from end"
        ),
        (
            "54321", 2,
            "321",
            "Edge case: Strictly decreasing - remove from start"
        ),
        (
            "10001", 1,
            "1",
            "Edge case: Multiple zeros"
        ),
        (
            "10", 1,
            "0",
            "Edge case: Two digits, remove one"
        ),
        (
            "9", 1,
            "0",
            "Edge case: Single digit, remove it"
        ),
        (
            "1111111", 3,
            "1111",
            "Edge case: All same digits"
        ),
        (
            "1234567890", 5,
            "12345",
            "Edge case: Long increasing then drop"
        ),
        (
            "1432219", 7,
            "0",
            "Edge case: Remove all digits (k = length)"
        ),
        (
            "100200", 1,
            "200",
            "Edge case: Remove leading 1 from 100200"
        ),
        (
            "120304", 3,
            "204",
            "Edge case: Mixed pattern"
        ),
    ]
    
    print("=" * 70)
    print("Running Tests for Remove K Digits (LeetCode 402)")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for i, (num, k, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.removeKdigits(num, k)
            if result == expected:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    Input:    num='{num}', k={k}")
                print(f"    Output:   '{result}'")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    Input:    num='{num}', k={k}")
                print(f"    Expected: '{expected}'")
                print(f"    Got:      '{result}'")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    Input:    num='{num}', k={k}")
            print(f"    Exception: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    run_tests()
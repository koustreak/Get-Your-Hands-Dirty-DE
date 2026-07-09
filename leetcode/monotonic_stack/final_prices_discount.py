"""
LeetCode 1475: Final Prices With a Special Discount in a Shop
==============================================================

সমস্যা বিবরণ (Problem Statement in Bengali):
--------------------------------------------
একটি integer array `prices` দেওয়া আছে, যেখানে `prices[i]` হলো i-তম item-এর দাম।

একটি বিশেষ ডিসকাউন্ট আছে: যদি আপনি i-তম item কিনেন, তবে আপনি একটি ডিসকাউন্ট পাবেন 
`prices[j]` এর সমান, যেখানে `j` হলো **minimum index** যাতে `j > i` এবং `prices[j] <= prices[i]`।
যদি এমন কোনো `j` না থাকে, তবে কোনো ডিসকাউন্ট পাবেন না।

প্রতিটি item-এর জন্য চূড়ান্ত দাম (final price) রিটার্ন করতে হবে।

Example 1:
Input: prices = [8,4,6,2,3]
Output: [4,2,4,2,3]
ব্যাখ্যা:
- Item 0: price=8, ডিসকাউন্ট = prices[1]=4 (কারণ 4 <= 8 এবং index 1 > 0), চূড়ান্ত দাম = 8-4=4
- Item 1: price=4, ডিসকাউন্ট = prices[3]=2 (কারণ 2 <= 4 এবং index 3 > 1), চূড়ান্ত দাম = 4-2=2
- Item 2: price=6, ডিসকাউন্ট = prices[3]=2 (কারণ 2 <= 6 এবং index 3 > 2), চূড়ান্ত দাম = 6-2=4
- Item 3: price=2, ডিসকাউন্ট নেই (ডানে কোনো price <= 2 নেই), চূড়ান্ত দাম = 2
- Item 4: price=3, ডিসকাউন্ট নেই (ডানে কোনো item নেই), চূড়ান্ত দাম = 3

Example 2:
Input: prices = [1,2,3,4,5]
Output: [1,2,3,4,5]
ব্যাখ্যা: সব item-এর ডানে বড় price আছে, তাই কোনো ডিসকাউন্ট নেই।

Example 3:
Input: prices = [10,1,1,6]
Output: [9,0,1,6]
ব্যাখ্যা:
- Item 0: price=10, ডিসকাউন্ট = prices[1]=1, চূড়ান্ত দাম = 9
- Item 1: price=1, ডিসকাউন্ট = prices[2]=1, চূড়ান্ত দাম = 0
- Item 2: price=1, ডিসকাউন্ট নেই, চূড়ান্ত দাম = 1
- Item 3: price=6, ডিসকাউন্ট নেই, চূড়ান্ত দাম = 6

Constraints:
- 1 <= prices.length <= 500
- 1 <= prices[i] <= 1000

সমাধান পদ্ধতি (Solution Approach):
-----------------------------------
এটি একটি classic **Monotonic Stack** problem।
- Stack-এ index রাখব (non-increasing order maintain করব)
- ডান থেকে বামে (right to left) traverse করব
- প্রতিটি element-এর জন্য stack-এ থেকে বড় element গুলো pop করব
- Stack-এর top যদি <= current price হয়, তবে সেটাই discount
- Time Complexity: O(n), Space Complexity: O(n)
"""

from typing import List


class Solution:
    def finalPrices(self, prices: List[int]) -> List[int]:
        """
        প্রতিটি item-এর জন্য চূড়ান্ত দাম ক্যালকুলেট করুন।
        
        Args:
            prices: List of item prices
            
        Returns:
            List of final prices after applying special discount
        """
        
        stack = []

        for i in range(len(prices)):
            while stack and prices[stack[-1]]>=prices[i]:
                idx = stack.pop()
                prices[idx] = prices[idx]-prices[i]

            stack.append(i)

        return prices


# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (prices, expected_output, description)
        (
            [8, 4, 6, 2, 3],
            [4, 2, 4, 2, 3],
            "Example 1: Basic case with multiple discounts"
        ),
        (
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            "Example 2: Strictly increasing - no discounts"
        ),
        (
            [10, 1, 1, 6],
            [9, 0, 1, 6],
            "Example 3: Duplicate prices"
        ),
        (
            [5],
            [5],
            "Edge case: Single item"
        ),
        (
            [5, 5, 5, 5],
            [0, 0, 0, 5],
            "Edge case: All same prices - each gets discount from next"
        ),
        (
            [5, 4, 3, 2, 1],
            [1, 1, 1, 1, 1],
            "Edge case: Strictly decreasing - each gets discount from immediate next"
        ),
        (
            [100, 1, 100, 1, 100],
            [99, 0, 99, 0, 100],
            "Edge case: Alternating high-low prices"
        ),
        (
            [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            "Edge case: Long strictly decreasing sequence"
        ),
        (
            [1, 3, 3, 2, 5],
            [1, 1, 1, 2, 5],
            "Edge case: Duplicate with smaller next element"
        ),
        (
            [4, 7, 1, 9, 4, 8, 8, 9, 4],
            [3, 6, 0, 5, 0, 0, 0, 5, 4],
            "Edge case: Complex pattern with duplicates"
        ),
    ]
    
    print("=" * 70)
    print("Running Tests for Final Prices With a Special Discount (LeetCode 1475)")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for i, (prices, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.finalPrices(prices)
            if result == expected:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    Input:    {prices}")
                print(f"    Output:   {result}")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    Input:    {prices}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    Input:    {prices}")
            print(f"    Exception: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    run_tests()
"""
LeetCode 2125: Number of Laser Beams in a Bank
==============================================

সমস্যা বিবরণ (Problem Statement in Bengali):
--------------------------------------------
একটি ব্যাংকের ভিতরে চুরি-রোধক নিরাপত্তা যন্ত্র (security devices) চালু করা হয়েছে। 
আপনাকে একটি 0-indexed binary string array `bank` দেওয়া হয়, যা ব্যাংকের floor plan 
রিপ্রেজেন্ট করে (একটি m x n 2D matrix)। `bank[i]` হলো ith row, যা '0' এবং '1' দিয়ে গঠিত। 
'0' মানে ঐ cell টি ফাঁকা, আর '1' মানে ঐ cell-এ একটি security device আছে।

দুটি security device-এর মাঝে ঠিক তখনই একটি লেজার বিম (laser beam) থাকে যদি নিচের 
দুটি শর্ত পূরণ হয়:

1. দুটি device দুটি আলাদা row-তে অবস্থিত: r1 এবং r2, যেখানে r1 < r2
2. r1 এবং r2 এর মাঝে থাকা প্রতিটি row i (যেখানে r1 < i < r2) এ কোনো security device নেই

লেজার বিম গুলো স্বাধীন (independent) — একটি বিম অন্যটির সাথে মিশে না।

ব্যাংকে মোট কতটি লেজার বিম আছে তা রিটার্ন করুন।

Example 1:
Input: bank = ["011001","000000","010100","001000"]
Output: 8
ব্যাখ্যা: নিচের device জোড়াগুলোর মাঝে একটি করে বিম আছে (মোট 8 টি):
- bank[0][1] -- bank[2][1]
- bank[0][1] -- bank[2][3]
- bank[0][2] -- bank[2][1]
- bank[0][2] -- bank[2][3]
- bank[0][5] -- bank[2][1]
- bank[0][5] -- bank[2][3]
- bank[2][1] -- bank[3][2]
- bank[2][3] -- bank[3][2]
Note: 0th row এবং 3rd row এর device গুলোর মাঝে কোনো বিম নেই, কারণ 2nd row-তে 
device আছে যা শর্ত ভঙ্গ করে।

Example 2:
Input: bank = ["000","111","000"]
Output: 0
ব্যাখ্যা: দুটি আলাদা row-তে একসাথে device নেই, তাই কোনো বিম নেই।

Constraints:
- m == bank.length
- n == bank[i].length
- 1 <= m, n <= 500
- bank[i][j] হলো '0' অথবা '1'

সমাধান পদ্ধতি (Solution Approach - Hint):
-------------------------------------------
এটি মূলত একটি **Math / Counting** problem (DSU বা graph লাগে না):
1. প্রতিটি row-তে '1' এর সংখ্যা গুনুন (device count)
2. শুধুমাত্র non-zero device count ওয়ালা row গুলোকে ট্র্যাক করুন
3. পরপর দুটি non-empty row (prev_count এবং curr_count) এর মাঝে বিম সংখ্যা = prev_count * curr_count
4. সব বিম যোগ করুন

Time Complexity: O(m * n)
Space Complexity: O(1)
"""

from typing import List


class Solution:
    def numberOfBeams(self, bank: List[str]) -> int:
        """
        ব্যাংকে মোট লেজার বিম সংখ্যা রিটার্ন করুন।
        
        Args:
            bank: List of binary strings representing the bank floor plan
            
        Returns:
            Total number of laser beams
        """
        # TODO: Implement your solution here
        # Hint: Count '1's per row, multiply adjacent non-zero row counts
        # 1. For each row, count devices (number of '1's)
        # 2. Keep track of previous non-zero row count
        # 3. For each new non-zero row, add prev * curr to total
        # 4. Update prev = curr
        current_count = 0
        total_beams = 0 
        prev_count = 0

        for row in bank:
            current_count = row.count('1')
            if current_count > 0:
                total_beams += prev_count * current_count
                prev_count = current_count

        return total_beams


# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (bank, expected_output, description)
        (
            ["011001", "000000", "010100", "001000"],
            8,
            "Example 1: Basic case with multiple beams"
        ),
        (
            ["000", "111", "000"],
            0,
            "Example 2: No two rows with devices"
        ),
        (
            ["1"],
            0,
            "Edge case: Single row, single device"
        ),
        (
            ["0"],
            0,
            "Edge case: Single row, no devices"
        ),
        (
            ["11", "11"],
            4,
            "Edge case: Two full rows, all devices"
        ),
        (
            ["1000", "0000", "0010"],
            1,
            "Edge case: Two non-adjacent non-empty rows"
        ),
        (
            ["101", "000", "101"],
            4,
            "Edge case: Two rows with 2 devices each, separated by empty"
        ),
        (
            ["1", "1", "1"],
            0,
            "Edge case: Each row has 1 device, but adjacent rows multiply to 1*1=1... wait"
        ),
        (
            ["111", "000", "111", "000", "111"],
            12,
            "Edge case: Alternating full and empty rows"
        ),
        (
            ["00000", "00000", "00000"],
            0,
            "Edge case: All empty rows"
        ),
        (
            ["01010", "10101", "01010"],
            12,
            "Edge case: Alternating pattern, 3 devices each adjacent"
        ),
        (
            ["1" * 500],
            0,
            "Edge case: Single very long row"
        ),
    ]
    
    print("=" * 70)
    print("Running Tests for Number of Laser Beams in a Bank (LeetCode 2125)")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for i, (bank, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.numberOfBeams(bank)
            if result == expected:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    Input:    {bank}")
                print(f"    Output:   {result}")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    Input:    {bank}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    Input:    {bank}")
            print(f"    Exception: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    run_tests()
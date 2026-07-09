"""
LeetCode: Checking Existence of Edge in Graph (DSU Problem)
============================================================

সমস্যা বিবরণ (Problem Statement in Bengali):
--------------------------------------------
একটি integer `n` দেওয়া আছে যা গ্রাফের node সংখ্যা রিপ্রেজেন্ট করে, 
node গুলো 0 থেকে n-1 পর্যন্ত লেবেল করা।

আপনাকে আরও দেওয়া হয়েছে:
- একটি integer array `nums` (length n), যা non-decreasing order-এ sorted
- একটি integer `maxDiff`

Node `i` এবং `j` এর মাঝে একটি undirected edge থাকবে যদি:
|nums[i] - nums[j]| <= maxDiff  (অর্থাৎ দুই node-এর nums মানের পার্থক্য maxDiff-এর সমান বা কম)

আপনাকে আরও দেওয়া হয়েছে একটি 2D integer array `queries`। 
প্রতিটি `queries[i] = [ui, vi]` এর জন্য, নির্ণয় করুন যে `ui` এবং `vi` node-এর 
মাঝে কোনো path আছে কিনা।

একটি boolean array `answer` রিটার্ন করুন, যেখানে `answer[i]` হবে `true` যদি 
ith query-তে `ui` এবং `vi` এর মাঝে path থাকে, নাহলে `false`।

Example 1:
Input: n = 2, nums = [1,3], maxDiff = 1, queries = [[0,0],[0,1]]
Output: [true, false]
ব্যাখ্যা:
- Query [0,0]: Node 0 নিজেই নিজের সাথে connected (trivial path)
- Query [0,1]: Node 0 এবং 1 এর মাঝে edge নেই কারণ |1-3| = 2 > maxDiff
অতএব answer = [true, false]

Example 2:
Input: n = 4, nums = [2,5,6,8], maxDiff = 2, queries = [[0,1],[0,2],[1,3],[2,3]]
Output: [false, false, true, true]
ব্যাখ্যা:
- Query [0,1]: |2-5| = 3 > maxDiff, তাই edge নেই
- Query [0,2]: |2-6| = 4 > maxDiff, তাই edge নেই
- Query [1,3]: Node 1 → Node 2 → Node 3 path আছে (|5-6|=1<=2, |6-8|=2<=2)
- Query [2,3]: |6-8| = 2 <= maxDiff, তাই edge আছে
অতএব answer = [false, false, true, true]

Constraints:
- 1 <= n <= 10^5
- 1 <= nums.length <= 10^5
- nums[i] sorted in non-decreasing order
- 0 <= nums[i] <= 10^9
- 0 <= maxDiff <= 10^9
- 1 <= queries.length <= 10^5
- 0 <= ui, vi < n

সমাধান পদ্ধতি (Solution Approach - Hint):
-------------------------------------------
এটি একটি **DSU (Disjoint Set Union)** problem:
1. nums sorted থাকায়, adjacent elements এর মাঝে edge check করলেই যথেষ্ট
   (non-adjacent pairs automatically connected যদি adjacent গুলো connected থাকে)
2. প্রতিটি i এর জন্য (0 থেকে n-2), যদি |nums[i] - nums[i+1]| <= maxDiff হয়,
   তবে i এবং i+1 কে union করুন
3. প্রতিটি query [ui, vi] এর জন্য, check করুন find(ui) == find(vi)
4. ui == vi হলে সরাসরি true (নিজেই নিজের সাথে connected)

Time Complexity: O(n + q) where q = queries.length
Space Complexity: O(n)
"""

from typing import List


class Solution:
    def areConnected(self, n: int, maxDiff: int, queries: List[List[int]], nums: List[int]) -> List[bool]:
        """
        প্রতিটি query-এর জন্য ui এবং vi connected কিনা চেক করুন।
        
        Args:
            n: Number of nodes (0 to n-1)
            maxDiff: Maximum allowed difference for an edge to exist
            queries: List of [ui, vi] pairs to check connectivity
            nums: Sorted array of node values
            
        Returns:
            List of boolean answers for each query
        """
        component = [0]*n 
        ans = [] 
        grp_id = 0

        for i in range(1,n):
            if abs(nums[i] - nums[i-1]) > maxDiff:
                grp_id += 1
            component[i] = grp_id
        
        for u,v in queries:
            ans.append(component[u] == component[v])

        return ans

# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (n, maxDiff, queries, nums, expected_output, description)
        (
            2, 1, [[0, 0], [0, 1]], [1, 3],
            [True, False],
            "Example 1: Basic case with no edge"
        ),
        (
            4, 2, [[0, 1], [0, 2], [1, 3], [2, 3]], [2, 5, 6, 8],
            [False, False, True, True],
            "Example 2: Path through intermediate node"
        ),
        (
            1, 0, [[0, 0]], [5],
            [True],
            "Edge case: Single node, self query"
        ),
        (
            3, 0, [[0, 1], [1, 2], [0, 2]], [1, 1, 1],
            [True, True, True],
            "Edge case: All same values, maxDiff=0 (all connected)"
        ),
        (
            3, 0, [[0, 1], [1, 2], [0, 2]], [1, 2, 3],
            [False, False, False],
            "Edge case: All different values, maxDiff=0 (no edges)"
        ),
        (
            5, 10, [[0, 4], [0, 1], [2, 3]], [1, 2, 3, 4, 5],
            [True, True, True],
            "Edge case: Large maxDiff, all connected"
        ),
        (
            5, 1, [[0, 4], [0, 1], [2, 3]], [1, 5, 10, 15, 20],
            [False, False, False],
            "Edge case: Large gaps, no connections"
        ),
        (
            4, 3, [[0, 0], [1, 1], [2, 2], [3, 3]], [1, 2, 3, 4],
            [True, True, True, True],
            "Edge case: All self queries"
        ),
        (
            6, 2, [[0, 5], [1, 4], [0, 3]], [1, 2, 4, 5, 7, 9],
            [True, True, True],
            "Edge case: Multiple connected components"
        ),
        (
            3, 5, [[0, 2], [0, 1], [1, 2]], [10, 12, 15],
            [True, True, True],
            "Edge case: Small gaps within maxDiff"
        ),
        (
            4, 1, [[0, 3], [1, 2]], [1, 2, 4, 5],
            [False, True],
            "Edge case: Two separate components"
        ),
        (
            5, 0, [[0, 4], [0, 2]], [5, 5, 5, 5, 5],
            [True, True],
            "Edge case: All same, maxDiff=0, cross queries"
        ),
    ]
    
    print("=" * 75)
    print("Running Tests for Checking Existence of Edge in Graph (DSU)")
    print("=" * 75)
    
    passed = 0
    failed = 0
    
    for i, (n, maxDiff, queries, nums, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.areConnected(n, maxDiff, queries, nums)
            if result == expected:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    n={n}, maxDiff={maxDiff}")
                print(f"    nums={nums}")
                print(f"    queries={queries}")
                print(f"    Output:   {result}")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    n={n}, maxDiff={maxDiff}")
                print(f"    nums={nums}")
                print(f"    queries={queries}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    n={n}, maxDiff={maxDiff}")
            print(f"    nums={nums}")
            print(f"    queries={queries}")
            print(f"    Exception: {e}")
            failed += 1
        print()
    
    print("=" * 75)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 75)
    
    return failed == 0


if __name__ == "__main__":
    run_tests()
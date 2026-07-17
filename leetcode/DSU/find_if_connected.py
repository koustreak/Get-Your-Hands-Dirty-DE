"""
LeetCode Style: Find If Two Nodes Are Connected (Easy DSU)
==========================================================

সমস্যা বিবরণ (Problem Statement in Bengali):
--------------------------------------------
একটি গ্রাফ দেওয়া আছে যা `n` টি node নিয়ে গঠিত (0 থেকে n-1 লেবেল করা)।
আপনাকে একটি edge list `edges` দেওয়া হয়, যেখানে প্রতিটি `edges[i] = [u, v]` 
বোঝায় যে node `u` এবং `v` সরাসরি connected।

একটি query `query = [a, b]` দেওয়া হয়। নির্ণয় করুন যে `a` এবং `b` 
সরাসরি বা পরোক্ষভাবে (intermediate node এর মাধ্যমে) connected কিনা।

যদি connected হয় `true`, নাহলে `false` রিটার্ন করুন।

Example 1:
Input: n = 5, edges = [[0,1],[1,2],[3,4]], query = [0,2]
Output: true
ব্যাখ্যা: 0 → 1 → 2 path আছে, তাই connected।

Example 2:
Input: n = 5, edges = [[0,1],[1,2],[3,4]], query = [0,4]
Output: false
ব্যাখ্যা: 0 এবং 4 আলাদা component-এ, তাই connected নয়।

Constraints:
- 1 <= n <= 1000
- 0 <= edges.length <= 5000
- 0 <= u, v < n
- 0 <= a, b < n

সমাধান পদ্ধতি (Solution Approach - Hint):
-------------------------------------------
এটি সবচেয়ে সহজ **DSU (Disjoint Set Union)** problem:
1. DSU initialize করুন n টি node দিয়ে
2. প্রতিটি edge [u, v] এর জন্য union(u, v) করুন
3. query [a, b] এর জন্য check করুন find(a) == find(b)

Time Complexity: O(n + e) where e = edges.length
Space Complexity: O(n)
"""

from typing import List


class Solution:
    def areNodesConnected(self, n: int, edges: List[List[int]], query: List[int]) -> bool:
        """
        দুটি node connected কিনা চেক করুন।
        
        Args:
            n: Number of nodes (0 to n-1)
            edges: List of [u, v] edges
            query: [a, b] - the two nodes to check
            
        Returns:
            True if a and b are connected, False otherwise
        """
        # TODO: Implement your solution here
        # Hint: Use DSU
        # 1. Initialize DSU with n nodes
        # 2. For each edge [u, v], union(u, v)
        # 3. Return find(a) == find(b) for query [a, b]
        pass


# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (n, edges, query, expected_output, description)
        (
            5, [[0, 1], [1, 2], [3, 4]], [0, 2],
            True,
            "Example 1: Path through intermediate node"
        ),
        (
            5, [[0, 1], [1, 2], [3, 4]], [0, 4],
            False,
            "Example 2: Separate components"
        ),
        (
            1, [], [0, 0],
            True,
            "Edge case: Single node, self query"
        ),
        (
            3, [], [0, 1],
            False,
            "Edge case: No edges at all"
        ),
        (
            4, [[0, 1], [1, 2], [2, 3]], [0, 3],
            True,
            "Edge case: Long chain all connected"
        ),
        (
            4, [[0, 1], [2, 3]], [1, 2],
            False,
            "Edge case: Two separate pairs"
        ),
        (
            6, [[0, 1], [1, 2], [3, 4], [4, 5]], [0, 5],
            False,
            "Edge case: Two long chains, not connected"
        ),
        (
            3, [[0, 1], [0, 2]], [1, 2],
            True,
            "Edge case: Star pattern (center 0)"
        ),
        (
            5, [[0, 1], [1, 2], [0, 3], [3, 4]], [2, 4],
            True,
            "Edge case: Complex tree, both connected"
        ),
        (
            2, [[0, 1]], [0, 1],
            True,
            "Edge case: Two nodes, one edge"
        ),
    ]
    
    print("=" * 70)
    print("Running Tests for Find If Two Nodes Are Connected (Easy DSU)")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for i, (n, edges, query, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.areNodesConnected(n, edges, query)
            if result == expected:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    n={n}, edges={edges}, query={query}")
                print(f"    Output:   {result}")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    n={n}, edges={edges}, query={query}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    n={n}, edges={edges}, query={query}")
            print(f"    Exception: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    run_tests()
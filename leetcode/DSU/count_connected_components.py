"""
LeetCode Style: Count Connected Components (Easy DSU)
=====================================================

সমস্যা বিবরণ (Problem Statement in Bengali):
--------------------------------------------
একটি গ্রাফ দেওয়া আছে যা `n` টি node নিয়ে গঠিত (0 থেকে n-1 লেবেল করা)।
আপনাকে একটি edge list `edges` দেওয়া হয়, যেখানে প্রতিটি `edges[i] = [u, v]` 
বোঝায় যে node `u` এবং `v` সরাসরি connected।

গ্রাফে মোট কতটি **connected component** (বিচ্ছিন্ন অংশ) আছে তা গুনে বের করুন।

Example 1:
Input: n = 5, edges = [[0,1],[1,2],[3,4]]
Output: 2
ব্যাখ্যা: {0,1,2} একটি component, {3,4} আরেকটি → মোট 2টি।

Example 2:
Input: n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]
Output: 1
ব্যাখ্যা: সব node একই component-এ যুক্ত → মোট 1টি।

Constraints:
- 1 <= n <= 1000
- 0 <= edges.length <= 5000
- 0 <= u, v < n

সমাধান পদ্ধতি (Solution Approach - Hint):
-------------------------------------------
এটি একটি সহজ **DSU (Disjoint Set Union)** problem:
1. DSU initialize করুন n টি node দিয়ে (count = n)
2. প্রতিটি edge [u, v] এর জন্য union(u, v) করুন (প্রতিবার successful union-এ count--)
3. DSU-এর count variable রিটার্ন করুন
   (অথবা সব node-এর unique root গুনুন)

Time Complexity: O(n + e) where e = edges.length
Space Complexity: O(n)
"""

from typing import List


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        """
        গ্রাফে মোট connected component সংখ্যা রিটার্ন করুন।
        
        Args:
            n: Number of nodes (0 to n-1)
            edges: List of [u, v] edges
            
        Returns:
            Number of connected components
        """
        # TODO: Implement your solution here
        # Hint: Use DSU
        # 1. Initialize DSU with n nodes (count = n)
        # 2. For each edge [u, v], union(u, v) and decrement count on success
        # 3. Return count (or count unique roots)
        pass


# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (n, edges, expected_output, description)
        (
            5, [[0, 1], [1, 2], [3, 4]],
            2,
            "Example 1: Two components"
        ),
        (
            5, [[0, 1], [1, 2], [2, 3], [3, 4]],
            1,
            "Example 2: Single connected component"
        ),
        (
            1, [],
            1,
            "Edge case: Single node, no edges"
        ),
        (
            4, [],
            4,
            "Edge case: All isolated nodes"
        ),
        (
            3, [[0, 1], [1, 2], [0, 2]],
            1,
            "Edge case: Triangle (fully connected)"
        ),
        (
            6, [[0, 1], [2, 3], [4, 5]],
            3,
            "Edge case: Three separate pairs"
        ),
        (
            4, [[0, 1], [2, 3]],
            2,
            "Edge case: Two separate pairs"
        ),
        (
            7, [[0, 1], [1, 2], [3, 4], [4, 5], [5, 6]],
            2,
            "Edge case: One chain of 3, one chain of 4"
        ),
        (
            5, [[0, 2], [1, 3], [2, 4]],
            2,
            "Edge case: Mixed connections"
        ),
        (
            3, [[0, 1], [0, 2], [1, 2]],
            1,
            "Edge case: Redundant edges, still 1 component"
        ),
    ]
    
    print("=" * 70)
    print("Running Tests for Count Connected Components (Easy DSU)")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for i, (n, edges, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.countComponents(n, edges)
            if result == expected:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    n={n}, edges={edges}")
                print(f"    Output:   {result}")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    n={n}, edges={edges}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    n={n}, edges={edges}")
            print(f"    Exception: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    run_tests()
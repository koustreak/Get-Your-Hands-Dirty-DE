"""
LeetCode 684: Redundant Connection
===================================

সমস্যা বিবরণ (Problem Statement in Bengali):
--------------------------------------------
একটি গ্রাফ দেওয়া আছে যা মূলত একটি tree ছিল, কিন্তু তাতে একটি extra edge যোগ করা হয়েছে। 
গ্রাফটি `n` টি node নিয়ে গঠিত (1 থেকে n পর্যন্ত লেবেল করা)।

আপনাকে একটি 2D integer array `edges` দেওয়া হয়, যা গ্রাফের সব edge গুলোর তালিকা 
(যার মাঝে একটি redundant/extra edge আছে)।

আপনার কাজ হলো সেই edge টি খুঁজে বের করা যা রিমুভ করলে গ্রাফটি আবার একটি valid tree হয়ে যাবে। 
যদি একাধিক সম্ভাব্য answer থাকে, তবে সেই edge টি রিটার্ন করুন যা `edges` array-তে 
সবচেয়ে শেষে (last) আছে।

Example 1:
Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]
ব্যাখ্যা: [2,3] রিমুভ করলে গ্রাফটি tree হয়ে যায়।

Example 2:
Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
Output: [1,4]
ব্যাখ্যা: [1,4] রিমুভ করলে গ্রাফটি valid tree হয়।

Constraints:
- 1 <= n <= 1000 (where n = number of nodes)
- edges.length == n (exactly one extra edge)
- edges[i].length == 2
- 1 <= ui, vi <= n
- ui != vi
- No duplicate edges initially

সমাধান পদ্ধতি (Solution Approach - Hint):
-------------------------------------------
এটি একটি classic **DSU (Disjoint Set Union)** problem for cycle detection:
1. DSU initialize করুন n টি node দিয়ে (1-indexed)
2. প্রতিটি edge [u, v] এর জন্য:
   - যদি find(u) == find(v), তবে এই edge টি cycle তৈরি করছে → এটিই redundant
   - নাহলে union(u, v) করুন
3. প্রথম যে edge টি cycle তৈরি করে, সেটি রিটার্ন করুন (কারণ আমরা edges 
   array-তে শেষে থাকা redundant edge চাই, তাই সব edge প্রসেস করে শেষটি রাখি)

Time Complexity: O(n * α(n))
Space Complexity: O(n)
"""

from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        """
        Redundant edge খুঁজে বের করুন যা রিমুভ করলে গ্রাফ tree হয়।
        
        Args:
            edges: List of edges in the graph (with one redundant edge)
            
        Returns:
            The redundant edge that appears last in the input
        """
        # TODO: Implement your solution here
        # Hint: Use DSU for cycle detection
        # 1. Initialize DSU with n nodes (n = max node value in edges)
        # 2. For each edge [u, v]:
        #    - If find(u) == find(v): this is the redundant edge, return it
        #    - Else: union(u, v)
        pass


# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (edges, expected_output, description)
        (
            [[1, 2], [1, 3], [2, 3]],
            [2, 3],
            "Example 1: Basic cycle"
        ),
        (
            [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],
            [1, 4],
            "Example 2: Cycle with extra branch"
        ),
        (
            [[1, 2], [2, 3], [3, 4], [4, 5], [5, 1]],
            [5, 1],
            "Edge case: Full cycle back to start"
        ),
        (
            [[1, 2], [1, 3], [1, 4], [2, 4]],
            [2, 4],
            "Edge case: Star with one extra edge"
        ),
        (
            [[1, 2], [3, 4], [2, 3], [1, 4]],
            [1, 4],
            "Edge case: Two pairs merged then cycle"
        ),
        (
            [[1, 2], [2, 3], [3, 1], [4, 5]],
            [3, 1],
            "Edge case: Cycle in first 3 nodes"
        ),
        (
            [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 3]],
            [6, 3],
            "Edge case: Longer chain with cycle"
        ),
        (
            [[1, 3], [3, 4], [1, 5], [3, 5], [2, 4]],
            [3, 5],
            "Edge case: Multiple possible, return last"
        ),
        (
            [[2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 2]],
            [7, 2],
            "Edge case: Cycle in larger graph"
        ),
        (
            [[1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 6]],
            [5, 6],
            "Edge case: Two branches meeting at end"
        ),
    ]
    
    print("=" * 70)
    print("Running Tests for Redundant Connection (LeetCode 684)")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for i, (edges, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.findRedundantConnection(edges)
            if result == expected:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    Input:    {edges}")
                print(f"    Output:   {result}")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    Input:    {edges}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    Input:    {edges}")
            print(f"    Exception: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    run_tests()
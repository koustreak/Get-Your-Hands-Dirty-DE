"""
LeetCode 547: Number of Provinces
==================================

সমস্যা বিবরণ (Problem Statement in Bengali):
--------------------------------------------
একটি দেশে `n` টি শহর আছে, যেগুলো 0 থেকে n-1 পর্যন্ত লেবেল করা। 
আমরা একটি 2D array `isConnected` দেওয়া পাই যার আকার n x n, যেখানে 
`isConnected[i][j] = 1` যদি শহর `i` এবং শহর `j` সরাসরি connected হয়, 
আর `isConnected[i][j] = 0` যদি না হয়।

দুটি শহর "প্রদেশ" (province) একই গ্রুপে পড়ে যদি তাদের মাঝে সরাসরি বা 
পরোক্ষভাবে (intermediate শহরের মাধ্যমে) সংযোগ থাকে।

মোট কতটি "প্রদেশ" (province) আছে তা রিটার্ন করুন।

Example 1:
Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
Output: 2
ব্যাখ্যা: শহর 0 এবং 1 connected (প্রদেশ 1), শহর 2 আলাদা (প্রদেশ 2)। মোট 2টি প্রদেশ।

Example 2:
Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
Output: 3
ব্যাখ্যা: কোনো শহরই connected নয়। 3টি আলাদা প্রদেশ।

Constraints:
- 1 <= n <= 200
- n == isConnected.length == isConnected[i].length
- isConnected[i][j] is 0 or 1
- isConnected[i][i] == 1 (নিজে নিজের সাথে connected)
- isConnected[i][j] == isConnected[j][i] (symmetric)

সমাধান পদ্ধতি (Solution Approach - Hint):
-------------------------------------------
এটি একটি classic **DSU (Disjoint Set Union)** problem:
1. DSU initialize করুন n টি node দিয়ে
2. প্রতিটি pair (i, j) এর জন্য যেখানে i < j এবং isConnected[i][j] == 1, 
   তাদের union করুন
3. DSU-এর count variable ট্র্যাক করুন (initially n), প্রতিবার successful union-এ 1 কমে
4. অথবা, সব node-এর unique root গুনুন

Time Complexity: O(n^2 * α(n))
Space Complexity: O(n)
"""

from typing import List


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        """
        মোট প্রদেশ (connected components) সংখ্যা রিটার্ন করুন।
        
        Args:
            isConnected: n x n adjacency matrix where 1 means connected
            
        Returns:
            Number of provinces (connected components)
        """
        # TODO: Implement your solution here
        # Hint: Use DSU
        # 1. Initialize DSU with n nodes
        # 2. For each pair (i, j) where i < j and isConnected[i][j] == 1, union(i, j)
        # 3. Count unique roots or use DSU's count variable
        pass


# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (isConnected, expected_output, description)
        (
            [[1, 1, 0], [1, 1, 0], [0, 0, 1]],
            2,
            "Example 1: Two provinces"
        ),
        (
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            3,
            "Example 2: Three isolated provinces"
        ),
        (
            [[1]],
            1,
            "Edge case: Single city"
        ),
        (
            [[1, 1], [1, 1]],
            1,
            "Edge case: Two fully connected cities"
        ),
        (
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            4,
            "Edge case: All isolated"
        ),
        (
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
            1,
            "Edge case: Fully connected (complete graph)"
        ),
        (
            [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]],
            2,
            "Edge case: Two separate pairs"
        ),
        (
            [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
            2,
            "Edge case: Chain 0-2 but 1 isolated"
        ),
        (
            [[1, 1, 0, 0, 0], [1, 1, 0, 0, 0], [0, 0, 1, 1, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 1]],
            3,
            "Edge case: Mixed components"
        ),
        (
            [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
            1,
            "Edge case: 4-node complete graph"
        ),
    ]
    
    print("=" * 70)
    print("Running Tests for Number of Provinces (LeetCode 547)")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for i, (isConnected, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.findCircleNum(isConnected)
            if result == expected:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    Input:    {isConnected}")
                print(f"    Output:   {result}")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    Input:    {isConnected}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    Input:    {isConnected}")
            print(f"    Exception: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    run_tests()
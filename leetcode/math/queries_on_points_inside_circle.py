"""
LeetCode 1828: Queries on Number of Points Inside a Circle
==========================================================

সমস্যা বিবরণ (Problem Statement in Bengali):
--------------------------------------------
একটি array `points` দেওয়া আছে যেখানে `points[i] = [xi, yi]` হলো 2D plane-এ 
ith point-এর কো-অর্ডিনেট। একাধিক point একই কো-অর্ডিনেটে থাকতে পারে।

আপনাকে আরও একটি array `queries` দেওয়া হয় যেখানে `queries[j] = [xj, yj, rj]` 
একটি circle কে রিপ্রেজেন্ট করে যার কেন্দ্র (xj, yj) এবং radius rj।

প্রতিটি query `queries[j]` এর জন্য, j-th circle-এর ভিতরে কতটি point আছে তা গুনুন। 
Circle-এর border-এ থাকা point গুলোকেও ভিতরে থাকা হিসেবে ধরা হয়।

একটি array `answer` রিটার্ন করুন, যেখানে `answer[j]` হলো j-th query-এর উত্তর।

Example 1:
Input: points = [[1,3],[3,3],[5,3],[2,2]], queries = [[2,3,1],[4,3,1],[1,1,2]]
Output: [3, 2, 2]
ব্যাখ্যা: 
- queries[0]: কেন্দ্র (2,3), r=1 → 3টি point ভিতরে (border সহ)
- queries[1]: কেন্দ্র (4,3), r=1 → 2টি point ভিতরে
- queries[2]: কেন্দ্র (1,1), r=2 → 2টি point ভিতরে

Example 2:
Input: points = [[1,1],[2,2],[3,3],[4,4],[5,5]], queries = [[1,2,2],[2,2,2],[4,3,2],[4,3,3]]
Output: [2, 3, 2, 4]
ব্যাখ্যা: চারটি query-এর জন্য যথাক্রমে 2, 3, 2, 4 টি point ভিতরে।

Constraints:
- 1 <= points.length <= 500
- points[i].length == 2
- 0 <= xi, yi <= 500
- 1 <= queries.length <= 500
- queries[j].length == 3
- 0 <= xj, yj <= 500
- 1 <= rj <= 500
- সব কো-অর্ডিনেট integer

সমাধান পদ্ধতি (Solution Approach - Hint):
-------------------------------------------
এটি একটি **Math / Geometry** problem:
1. প্রতিটি query [xj, yj, rj] এর জন্য:
2. প্রতিটি point [xi, yi] এর জন্য দূরত্ব চেক করুন:
   - Euclidean distance squared: (xi - xj)² + (yi - yj)² <= rj²
   - Square root না নিয়ে squared form ব্যবহার করুন (precision issue এড়াতে)
3. যে সব point শর্ত পূরণ করে, তাদের সংখ্যা গুনুন
4. প্রতিটি query-এর জন্য count রিটার্ন করুন

Time Complexity: O(q * p) where q = queries.length, p = points.length
Space Complexity: O(q) for the answer array
"""

from typing import List


import bisect

class Solution:
    def countPoints(self, points: list[list[int]], queries: list[list[int]]) -> list[int]:
        # ১. পয়েন্টগুলোকে X-coordinate অনুযায়ী সর্ট করুন
        points.sort(key=lambda p: p[0])
        
        # শুধু X-স্থানাঙ্কগুলোর একটি আলাদা লিস্ট তৈরি করুন (Binary Search এর জন্য)
        x_coords = [p[0] for p in points]
        answer = []
        
        for xj, yj, rj in queries:
            count = 0
            r_squared = rj * rj
            
            # ২. বৃত্তের X-সীমা নির্ধারণ করুন
            min_x = xj - rj
            max_x = xj + rj
            
            # ৩. Binary Search দিয়ে শুধু প্রয়োজনীয় পয়েন্টের রেঞ্জ খুঁজে নিন
            left_idx = bisect.bisect_left(x_coords, min_x)
            right_idx = bisect.bisect_right(x_coords, max_x)
            
            # ৪. শুধু এই রেঞ্জের ভেতরের পয়েন্টগুলোর দূরত্বের সূত্র চেক করুন
            for i in range(left_idx, right_idx):
                xi, yi = points[i]
                if (xi - xj)**2 + (yi - yj)**2 <= r_squared:
                    count += 1
                    
            answer.append(count)
            
        return answer



# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (points, queries, expected_output, description)
        (
            [[1, 3], [3, 3], [5, 3], [2, 2]],
            [[2, 3, 1], [4, 3, 1], [1, 1, 2]],
            [3, 2, 2],
            "Example 1: Basic case"
        ),
        (
            [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]],
            [[1, 2, 2], [2, 2, 2], [4, 3, 2], [4, 3, 3]],
            [2, 3, 2, 4],
            "Example 2: Multiple queries"
        ),
        (
            [[0, 0]],
            [[0, 0, 1]],
            [1],
            "Edge case: Single point at center"
        ),
        (
            [[10, 10]],
            [[0, 0, 1]],
            [0],
            "Edge case: Point far outside circle"
        ),
        (
            [[0, 0], [0, 0], [0, 0]],
            [[0, 0, 5]],
            [3],
            "Edge case: Duplicate points all inside"
        ),
        (
            [[1, 0], [0, 1], [-1, 0], [0, -1]],
            [[0, 0, 1]],
            [4],
            "Edge case: Points exactly on border (radius 1)"
        ),
        (
            [[5, 5], [5, 5]],
            [[5, 5, 0]],
            [2],
            "Edge case: Radius 0, points at center"
        ),
        (
            [[1, 1], [2, 2], [3, 3]],
            [[0, 0, 1], [0, 0, 2], [0, 0, 3], [0, 0, 4]],
            [0, 1, 2, 3],
            "Edge case: Increasing radius captures more"
        ),
        (
            [[100, 100], [200, 200]],
            [[150, 150, 50], [150, 150, 100]],
            [0, 2],
            "Edge case: Large coordinates"
        ),
        (
            [[0, 0], [1, 1], [2, 2], [3, 3]],
            [[1, 1, 1], [2, 2, 2]],
            [2, 4],
            "Edge case: Overlapping circles"
        ),
    ]
    
    print("=" * 75)
    print("Running Tests for Queries on Points Inside a Circle (LeetCode 1828)")
    print("=" * 75)
    
    passed = 0
    failed = 0
    
    for i, (points, queries, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.countPoints(points, queries)
            if result == expected:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    points={points}")
                print(f"    queries={queries}")
                print(f"    Output:   {result}")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    points={points}")
                print(f"    queries={queries}")
                print(f"    Expected: {expected}")
                print(f"    Got:      {result}")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    points={points}")
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
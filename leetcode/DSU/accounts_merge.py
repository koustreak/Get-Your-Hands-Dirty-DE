"""
LeetCode 721: Accounts Merge
=============================

সমস্যা বিবরণ (Problem Statement in Bengali):
--------------------------------------------
একটি list of accounts দেওয়া আছে, যেখানে প্রতিটি account হলো:
`accounts[i] = [name_i, email1_i, email2_i, ...]` (একজন ব্যবহারকারীর নাম + তার emails)

দুটি account একই ব্যক্তির যদি:
1. তাদের নাম একই হয়, এবং
2. তাদের অন্তত একটি email address মিল থাকে

একই ব্যক্তির সব account কে একত্রিত (merge) করতে হবে। 
মনে রাখবেন, একই ব্যক্তির দুটি account সরাসরি না মিললেও, 
তৃতীয় একটি account এর মাধ্যমে পরোক্ষভাবে (transitive) যুক্ত থাকতে পারে।

প্রতিটি merged account ফরম্যাটে রিটার্ন করুন:
`[name, email1, email2, ...]` যেখানে emails গুলো sorted (ascending) থাকবে।

Example 1:
Input: accounts = [
  ["John", "johnsmith@mail.com", "john00@mail.com"],
  ["John", "johnnybravo@mail.com"],
  ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
  ["Mary", "mary@mail.com"]
]
Output: [
  ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
  ["John", "johnnybravo@mail.com"],
  ["Mary", "mary@mail.com"]
]
ব্যাখ্যা: প্রথম ও তৃতীয় John account একই (johnsmith@mail.com শেয়ার করে) → merge করা হয়েছে।

Example 2:
Input: accounts = [
  ["Gabe", "gabe@mail.com", "robert@mail.com", "gabriel@mail.com"],
  ["Gabe", "gabe@mail.com", "bob@mail.com"]
]
Output: [
  ["Gabe", "bob@mail.com", "gabe@mail.com", "gabriel@mail.com", "robert@mail.com"]
]
ব্যাখ্যা: দুটি Gabe account একই (gabe@mail.com শেয়ার করে) → সব email merge।

Constraints:
- 1 <= accounts.length <= 1000
- 2 <= accounts[i].length <= 10
- accounts[i][0] is name (non-empty string)
- accounts[i][j] (j >= 1) are emails (valid email format)
- Length of each email < 30
- At most 10000 emails total

সমাধান পদ্ধতি (Solution Approach - Hint):
-------------------------------------------
এটি একটি **DSU (Disjoint Set Union)** problem for equivalence classes:
1. প্রতিটি unique email কে একটি node হিসেবে treat করুন
2. DSU initialize করুন (email → index mapping ব্যবহার করুন)
3. প্রতিটি account-এর সব email কে আপসে pairwise union করুন 
   (প্রথম email এর সাথে বাকি সব email union করলেই যথেষ্ট)
4. প্রতিটি root-এর অধীনে থাকা সব email গুনে রাখুন (dictionary ব্যবহার করে)
5. প্রতিটি connected component এর জন্য: name + sorted emails দিয়ে result বানান

Time Complexity: O(n * m * α(n)) where n = accounts, m = avg emails per account
Space Complexity: O(total emails)
"""

from typing import List


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        """
        একই ব্যক্তির সব account একত্রিত করে রিটার্ন করুন।
        
        Args:
            accounts: List of [name, email1, email2, ...] accounts
            
        Returns:
            List of merged accounts with sorted emails
        """
        parent = {}
        


# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (accounts, expected_output, description)
        (
            [
                ["John", "johnsmith@mail.com", "john00@mail.com"],
                ["John", "johnnybravo@mail.com"],
                ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
                ["Mary", "mary@mail.com"]
            ],
            [
                ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
                ["John", "johnnybravo@mail.com"],
                ["Mary", "mary@mail.com"]
            ],
            "Example 1: Basic merge with transitive connection"
        ),
        (
            [
                ["Gabe", "gabe@mail.com", "robert@mail.com", "gabriel@mail.com"],
                ["Gabe", "gabe@mail.com", "bob@mail.com"]
            ],
            [
                ["Gabe", "bob@mail.com", "gabe@mail.com", "gabriel@mail.com", "robert@mail.com"]
            ],
            "Example 2: Two accounts merge into one"
        ),
        (
            [
                ["John", "a@mail.com"],
                ["John", "b@mail.com"],
                ["John", "c@mail.com"]
            ],
            [
                ["John", "a@mail.com"],
                ["John", "b@mail.com"],
                ["John", "c@mail.com"]
            ],
            "Edge case: Same name, no shared emails (separate)"
        ),
        (
            [
                ["Alice", "alice@mail.com", "alice2@mail.com"],
                ["Bob", "bob@mail.com"],
                ["Alice", "alice2@mail.com", "alice3@mail.com"]
            ],
            [
                ["Alice", "alice2@mail.com", "alice3@mail.com", "alice@mail.com"],
                ["Bob", "bob@mail.com"]
            ],
            "Edge case: Transitive merge across 3 accounts"
        ),
        (
            [
                ["David", "d@mail.com"],
                ["David", "d@mail.com"]
            ],
            [
                ["David", "d@mail.com"]
            ],
            "Edge case: Duplicate account (same email)"
        ),
        (
            [
                ["Eve", "e1@mail.com", "e2@mail.com", "e3@mail.com"],
                ["Eve", "e3@mail.com", "e4@mail.com"],
                ["Eve", "e4@mail.com", "e5@mail.com"]
            ],
            [
                ["Eve", "e1@mail.com", "e2@mail.com", "e3@mail.com", "e4@mail.com", "e5@mail.com"]
            ],
            "Edge case: Chain of 5 emails merged"
        ),
        (
            [
                ["Tom", "t@mail.com"],
                ["Jerry", "j@mail.com"],
                ["Tom", "t2@mail.com"],
                ["Jerry", "j2@mail.com"]
            ],
            [
                ["Tom", "t@mail.com"],
                ["Jerry", "j@mail.com"],
                ["Tom", "t2@mail.com"],
                ["Jerry", "j2@mail.com"]
            ],
            "Edge case: Multiple people, no merges"
        ),
        (
            [
                ["Sam", "s1@mail.com", "s2@mail.com"],
                ["Sam", "s2@mail.com", "s3@mail.com"],
                ["Sam", "s3@mail.com", "s4@mail.com"],
                ["Sam", "s4@mail.com", "s5@mail.com"]
            ],
            [
                ["Sam", "s1@mail.com", "s2@mail.com", "s3@mail.com", "s4@mail.com", "s5@mail.com"]
            ],
            "Edge case: Long chain merge"
        ),
    ]
    
    print("=" * 70)
    print("Running Tests for Accounts Merge (LeetCode 721)")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for i, (accounts, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.accountsMerge(accounts)
            # Sort result by name and first email for consistent comparison
            result_sorted = sorted(result, key=lambda x: (x[0], x[1]))
            expected_sorted = sorted(expected, key=lambda x: (x[0], x[1]))
            if result_sorted == expected_sorted:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    Output:   {result_sorted}")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    Expected: {expected_sorted}")
                print(f"    Got:      {result_sorted}")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    Input:    {accounts}")
            print(f"    Exception: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    run_tests()
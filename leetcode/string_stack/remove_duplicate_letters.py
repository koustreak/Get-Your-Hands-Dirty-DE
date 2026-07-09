"""
LeetCode 316: Remove Duplicate Letters
=======================================

সমস্যা বিবরণ (Problem Statement in Bengali):
--------------------------------------------
একটি string `s` দেওয়া আছে। ডুপ্লিকেট লেটার গুলো রিমুভ করুন যাতে প্রতিটি লেটার 
শুধু একবার করে থাকে। আপনাকে নিশ্চিত করতে হবে যে আপনার রেজাল্ট সব সম্ভাব্য 
রেজাল্টের মধ্যে **lexicographically smallest** (শব্দকোষ অনুযায়ী সবচেয়ে ছোট)।

Example 1:
Input: s = "bcabc"
Output: "abc"
ব্যাখ্যা: সম্ভাব্য রেজাল্ট গুলো: "abc", "bac", "cab", "cba"। 
Lexicographically smallest হলো "abc"।

Example 2:
Input: s = "cbacdcbc"
Output: "acdb"
ব্যাখ্যা: সম্ভাব্য রেজাল্ট গুলোর মধ্যে "acdb" সবচেয়ে ছোট।

Constraints:
- 1 <= s.length <= 10^4
- s শুধু lowercase English letters দিয়ে গঠিত

সমাধান পদ্ধতি (Solution Approach):
-----------------------------------
এটি একটি **Monotonic Stack** problem with greedy approach:
1. প্রতিটি character-এর last occurrence index ট্র্যাক করুন
2. Stack ব্যবহার করুন (monotonic increasing order maintain করব)
3. Visited set ব্যবহার করুন যাতে duplicate add না হয়
4. প্রতিটি character-এর জন্য:
   - যদি ইতিমধ্যে visited থাকে, skip করুন
   - Stack খালি না হলে এবং current char < stack top এবং 
     stack top এর last occurrence > current index হলে, stack top কে pop করুন
   - Current char কে stack-এ push করুন এবং visited mark করুন
5. Stack কে join করে string বানান

Time Complexity: O(n), Space Complexity: O(1) - শুধু 26 letters
"""

from typing import List


class Solution:
    def removeDuplicateLetters(self, s: str) -> str:
        """
        ডুপ্লিকেট লেটার রিমুভ করে lexicographically smallest string রিটার্ন করুন।
        
        Args:
            s: Input string with lowercase letters
            
        Returns:
            String with each letter appearing once, lexicographically smallest
        """
        
        last_ocr = {char:i for i,char in enumerate(s)}

        stack = []
        visited = set()

        for i,char in enumerate(s):
            if char in visited:
                continue 

            while stack and stack[-1]>char and last_ocr[stack[-1]]>i:
                visited.remove(stack.pop())
                stack.pop()

            stack.append(char)
            visited.add(char)

        return ''.join(stack)

# ============================================================
# TEST STUB - Run this file to test your solution
# ============================================================
def run_tests():
    """Test cases including edge cases"""
    solution = Solution()
    
    test_cases = [
        # (input, expected_output, description)
        (
            "bcabc",
            "abc",
            "Example 1: Basic case"
        ),
        (
            "cbacdcbc",
            "acdb",
            "Example 2: Complex case with multiple duplicates"
        ),
        (
            "a",
            "a",
            "Edge case: Single character"
        ),
        (
            "aa",
            "a",
            "Edge case: All same characters"
        ),
        (
            "abacb",
            "abc",
            "Edge case: Repeating pattern"
        ),
        (
            "bbcaac",
            "bac",
            "Edge case: Multiple duplicates"
        ),
        (
            "abcdefghijklmnopqrstuvwxyz",
            "abcdefghijklmnopqrstuvwxyz",
            "Edge case: All unique characters (already sorted)"
        ),
        (
            "zyxwvutsrqponmlkjihgfedcba",
            "zyxwvutsrqponmlkjihgfedcba",
            "Edge case: All unique characters (reverse sorted)"
        ),
        (
            "aaaaaaaa",
            "a",
            "Edge case: Many duplicates of same char"
        ),
        (
            "abacaba",
            "abc",
            "Edge case: Palindrome-like pattern"
        ),
        (
            "leetcode",
            "letcod",
            "Edge case: Word with duplicates"
        ),
        (
            "ecbacba",
            "eacb",
            "Edge case: Starting with larger char"
        ),
    ]
    
    print("=" * 70)
    print("Running Tests for Remove Duplicate Letters (LeetCode 316)")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for i, (s, expected, description) in enumerate(test_cases, 1):
        try:
            result = solution.removeDuplicateLetters(s)
            if result == expected:
                print(f"✅ Test {i:2d} PASSED: {description}")
                print(f"    Input:    '{s}'")
                print(f"    Output:   '{result}'")
                passed += 1
            else:
                print(f"❌ Test {i:2d} FAILED: {description}")
                print(f"    Input:    '{s}'")
                print(f"    Expected: '{expected}'")
                print(f"    Got:      '{result}'")
                failed += 1
        except Exception as e:
            print(f"❌ Test {i:2d} ERROR: {description}")
            print(f"    Input:    '{s}'")
            print(f"    Exception: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    run_tests()
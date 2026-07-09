"""
LeetCode 1288: Remove Covered Intervals
========================================

সমস্যা বিবরণ (Problem Statement in Bengali):
------------------------------------------
একটি intervals array দেওয়া আছে, যেখানে intervals[i] = [li, ri] 
ইন্টারভাল [li, ri) কে প্রতিনিধিত্ব করে। 
সকল ইন্টারভাল যেগুলো অন্য কোনো ইন্টারভাল দ্বারা covered (আচ্ছাদিত) হয়েছে, 
তাদের রিমুভ করতে হবে।

ইন্টারভাল [a, b) ইন্টারভাল [c, d) দ্বারা covered হয় যদি এবং কেবল যদি:
c <= a এবং b <= d

অবশিষ্ট ইন্টারভালের সংখ্যা রিটার্ন করতে হবে।

Example 1:
Input: intervals = [[1,4],[3,6],[2,8]]
Output: 2
ব্যাখ্যা: ইন্টারভাল [3,6] ইন্টারভাল [2,8] দ্বারা covered, তাই এটি রিমুভ হয়।

Example 2:
Input: intervals = [[1,4],[2,3]]
Output: 1

Constraints:
- 1 <= intervals.length <= 1000
- intervals[i].length == 2
- 0 <= li < ri <= 10^5
- সব দেওয়া ইন্টারভালগুলো unique

সমাধান পদ্ধতি (Solution Approach):
-----------------------------------
1. ইন্টারভালগুলোকে start ascending, end descending অর্ডারে সর্ট করুন
2. সর্বোচ্চ end ট্র্যাক করুন
3. যদি বর্তমান ইন্টারভালের end <= max_end হয়, তবে এটি covered
4. অন্যথায়, max_end আপডেট করুন এবং count বাড়ান

Time Complexity: O(n log n) - সর্টিং এর কারণে
Space Complexity: O(1) - অতিরিক্ত স্পেস ব্যবহার হয়নি
"""

from typing import List


class Solution:
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        """
        Covered intervals রিমুভ করে অবশিষ্ট ইন্টারভালের সংখ্যা রিটার্ন করে।
        
        Args:
            intervals: List of [start, end] pairs representing intervals [start, end)
            
        Returns:
            Number of remaining intervals after removing covered ones
        """
        # Start ascending, end descending অর্ডারে সর্ট করুন
        # Start একই হলে, বড় end वाला আগে আসবে (যাতে সেটা অন্যদের cover করতে পারে)
        intervals.sort(key=lambda x: (x[0], -x[1]))
        
        count = 0
        max_end = -1
        
        for start, end in intervals:
            # যদি বর্তমান interval-এর end <= max_end হয়, 
            # তবে এটি আগের কোনো interval দ্বারা covered
            if end <= max_end:
                continue  # covered interval, skip করুন
            
            # Covered নয়, তাই count বাড়ান এবং max_end আপডেট করুন
            count += 1
            max_end = end
        
        return count


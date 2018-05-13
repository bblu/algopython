
# Given a string, find the length of the longest substring without repeating characters.
#
# Examples:
# Given "abcabcbb", the answer is "abc", which the length is 3.
# Given "bbbbb", the answer is "b", with the length of 1.
# Given "pwwkew", the answer is "wke", with the length of 3. Note that the answer must be a substring, "pwke" is a subsequence and not a substring.

class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        maxLen, curPos, charPos= 0, 0, {}
        for idx, char in enumerate(s, 1):
            if charPos.get(char, -1) >= curPos:
                curPos = charPos[char]
            charPos[char] = idx
            maxLen = max(maxLen, idx - curPos)
        return maxLen


if __name__ == "__main__":
    sol = Solution()
    s = 'aabcdd'
    l = sol.lengthOfLongestSubstring(s)
    print l
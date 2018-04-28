'''Given an array of integers with possible duplicates, randomly output the index of a given target number.
You can assume that the given target number must exist in the array.

Note:
The array size can be very large. Solution that uses too much extra space will not pass the judge.

Example:

int[] nums = new int[] {1,2,3,3,3};
Solution solution = new Solution(nums);

// pick(3) should return either index 2, 3, or 4 randomly. Each index should have equal probability of returning.
solution.pick(3);

// pick(1) should return 0. Since in the array only nums[0] is equal to 1.
solution.pick(1);
'''
import random

class Solution0(object):
    singles = {}
    randoms = {}
    def __init__(self, nums):
        """

        :type nums: List[int]
        :type numsSize: int
        """
        for idx, tar in enumerate(nums):
            if tar in self.singles.keys():
                self.randoms[tar] = []
                self.randoms[tar].append(self.singles[tar])
                del self.singles[tar]
                print 'rmv %s to randoms idx=%s and singles=%s' % (tar, self.randoms[tar], self.singles)
                self.randoms[tar].append(idx)
                print 'put %s in randoms idx=%s' % (tar, self.randoms[tar])
            elif tar in self.randoms.keys():
                self.randoms[tar].append(idx)
                print 'put %s in randoms idx=%s' % (tar, self.randoms[tar])
            else:
                print 'put %s in singles idx=%s' % (tar, idx)
                self.singles[tar] = idx;

    def pick(self, target):
        """
        :type target: int
        :rtype: int
        """
        if target in self.singles.keys():
            return self.singles[target]
        idx = self.randoms[target][0]
        self.randoms[target].append(self.randoms[target].pop(0))
        return idx


class Solution(object):
    nums = []

    def __init__(self, nums):
        self.nums = nums

    def pick(self, target):
        cnt = 0
        res = -1
        for i, t in enumerate(self.nums):
            if t == target:
                cnt += 1
                if random.randrange(cnt) == 0:
                    res = i
        return res


    # Your Solution object will be instantiated and called as such:
    # obj = Solution(nums)
    # param_1 = obj.pick(target)
if __name__ == '__main__':
    nums = [1, 2, 3, 3, 3]
    obj = Solution(nums)
    p = obj.pick(2)
    print p
    for i in range(5):
        print i, obj.pick(3)
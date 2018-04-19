# getIndicesByTarget.py @ 2018-4-19 23:27

class Solution:
    def getIndicesByTarget(self,nums,tar):
        diff = -1
        indices = []
        for i,v in enumerate(nums):
            if v < tar:
                indices.append(i)
                tar = tar - v 
            elif v == tar:
                indices.append(i)
                return indices

if __name__ == '__main__':
    mySolution = Solution()
    nums = [2,10,7,5,8]
    tar = 7
    indices = mySolution.getIndicesByTarget(nums,tar)
    if len(indices) == 2:
        print indices
    else:
        print 'sory world!'


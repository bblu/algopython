# getIndicesByTarget.py @ 2018-4-19 23:27

class Solution:
    def getIndicesByTarget(self,nums,tar):
        for base in range(0,len(nums)):
            p0,p1 = -1,-1
            print '|-deal with base=%s' % base
            subNums = nums[base:] 
            for i,v in enumerate(subNums):
                if p0 < 0 and v < tar:
                    p0 = base + i
                    print '|--p0=%s'%p0
                    p1 = tar - v 
                elif v == p1:
                    print '|-find index:base=%s' % base
                    return [p0, base+i]
            print '|-not find index:base=%s' % base
        return [p0,p1]

if __name__ == '__main__':
    mySolution = Solution()
    nums = [1,2,10,7,5,8]
    tar = 7
    indices = mySolution.getIndicesByTarget(nums,tar)
    if len(indices) == 2:
        print(indices)
    else:
        print('sory world!')


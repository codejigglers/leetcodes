class Solution(object):
    def hammingWeight(self, n):
        count=0

        while (n!=0):
            if(n & 1):
               count+=1
            n = n >> 1
        return count

var=Solution()
print(var.hammingWeight(11))
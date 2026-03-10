#using dict is alot more efficient than O(n^2) checking
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

                 
        visited = {} #{item: index}

        length = len(nums)
        for index in range(length):

            current = nums[index]

            query = target - current

            if query in visited:
                return [index, visited[query]] 
            else:
                visited[current] = index
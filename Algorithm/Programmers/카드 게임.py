import sys
sys.setrecursionlimit(10**6)

def solution(left, right):
    dp = [[-1]*len(right) for _ in range(len(left))]
    def solve(left_idx, right_idx):
        nonlocal dp
        if left_idx == len(left) or right_idx == len(right):
            return 0
        if dp[left_idx][right_idx] != -1:
            return dp[left_idx][right_idx]
        ret = 0
        if left[left_idx] > right[right_idx]:
            ret = solve(left_idx, right_idx+1) + right[right_idx]
            dp[left_idx][right_idx] = ret
        else:
            ret = max(solve(left_idx+1, right_idx), solve(left_idx+1, right_idx+1))
            dp[left_idx][right_idx] = ret
        return ret
    return solve(0, 0)
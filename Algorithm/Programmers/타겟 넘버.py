def solution(numbers, target):
    answer = 0
    def solve(idx=0):
        nonlocal numbers, target, answer
        if idx == len(numbers):
            if sum(numbers) == target:
                answer += 1
            return
        solve(idx+1)
        numbers[idx] *= -1
        solve(idx+1)
    solve()
    return answer
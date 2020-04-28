def solution(budgets, M):
    answer = 0
    left, right = 0, max(budgets)
    while left <= right:
        tmp = 0
        mid = (left + right) // 2
        for budget in budgets:
            if budget < mid:
                tmp += budget
            else:
                tmp += mid
        if tmp > M:
            right = mid - 1
        else:
            left = mid + 1
            answer = mid
    return answer
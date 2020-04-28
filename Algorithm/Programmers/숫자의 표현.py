def solution(n):
    answer = 0
    for start in range(1, n+1):
        sum_ = 0
        while sum_ < n:
            sum_ += start
            start += 1
        if sum_ == n:
            answer += 1
    return answer
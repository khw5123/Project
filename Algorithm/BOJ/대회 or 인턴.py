def solution(n, m, k):
    for i in range(m, 0, -1):
        if n >= m*2:
            k -= n-m*2
            break
        else:
            m, k = m-1, k-1
    if k > 0:
        m -= k//3
        if k%3 != 0:
            m -= 1
    return m

n, m, k = map(int, input().split())
print(solution(n, m, k))
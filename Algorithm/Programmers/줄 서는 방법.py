def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

def solution(n, k):
    answer = []
    m = n
    formula = factorial(n)
    while n != 0:
        prev = formula
        formula //= n
        tmp = list()
        for i in range(1, m+1):
            if i not in answer:
                tmp.append(i)
        idx = 0
        for i in range(0, prev, formula):
            if k >= i and k <= i+formula:
                answer.append(tmp[idx])
                k -= i
                break
            idx += 1
        n -= 1
    return answer
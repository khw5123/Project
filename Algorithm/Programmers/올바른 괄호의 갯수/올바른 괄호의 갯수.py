def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)

def solution(n):
    answer = factorial(2*n) // (factorial(n+1) * factorial(n))
    return answer

'''
import copy

def identify(s):
    a = copy.deepcopy(s)
    while len(a) != 0:
        tmp = len(a)
        for i in range(len(a)-1):
            if a[i] == '(' and a[i+1] == ')':
                del a[i]
                del a[i]
                break
        if tmp == len(a):
            return False
    return True

def solve(m, s, n):
    if m == n:
        if identify(s):
            return 1
        return 0
    answer = 0
    confirm = 0
    for i in range(len(s)):
        if s[i] == '(':
            confirm += 1
        else:
            confirm -= 1
        if confirm < 0:
            return 0
        if i+1 == len(s) // 2:
            if len(s) // 2 < confirm:
                return 0
    s.append('(')
    s.append(')')
    answer += solve(m + 1, s, n)
    s.pop()
    s.pop()
    s.append('(')
    s.append('(')
    answer += solve(m + 1, s, n)
    s.pop()
    s.pop()
    s.append(')')
    s.append(')')
    answer += solve(m + 1, s, n)
    s.pop()
    s.pop()
    s.append(')')
    s.append('(')
    answer += solve(m + 1, s, n)
    s.pop()
    s.pop()
    return answer

def solution(n):
    answer = solve(0, [], n)
    return answer
'''
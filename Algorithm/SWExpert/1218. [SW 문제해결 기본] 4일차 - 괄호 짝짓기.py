def solve(a, b):
    result = 1
    stack = []
    for i in range(n):
        if s[i] == a:
            stack.append(s[i])
        elif s[i] == b:
            if len(stack):
                stack.pop()
            else:
                result = 0
                break
    if len(stack):
        result = 0
    return result

for t in range(10):
    n = int(input())
    s = input()
    answer = 1
    if not solve('(', ')') or not solve('[', ']') or not solve('{', '}') or not solve('<', '>'):
        answer = 0
    print('#' + str(t+1), str(answer))
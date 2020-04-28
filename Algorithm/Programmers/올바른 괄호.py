def solution(s):
    answer = True
    stack = list()
    for c in s:
        if c == ')' and len(stack) != 0 and stack[-1] == '(':
            stack.pop()
        elif c == ')' and len(stack) != 0 and stack[-1] != '(':
            stack.append(')')
        else:
            stack.append('(')
    if len(stack) != 0:
        answer = False
    return answer
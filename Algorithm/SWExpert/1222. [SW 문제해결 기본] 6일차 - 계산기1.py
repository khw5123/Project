def solve(op1, op2):
    result = False
    if op1 != '(' and op1 != []:
        if di[op1] >= di[op2]:
            result = True
    return result

for t in range(10):
    di = {'+':1, '-':1, '*':2, '/':2}
    n = int(input())
    s = input()
    postfix_expression = []
    stack = []
    for i in range(len(s)):
        if s[i] not in '+-*/()':
            postfix_expression.append(s[i])
        else:
            if s[i] == '(':
                stack.append(s[i])
            elif s[i] == ')':
                while True:
                    if stack[-1] == '(':
                        stack.pop()
                        break
                    postfix_expression.append(stack[-1])
                    stack.pop()
            else:
                while True:
                    if not len(stack) or not solve(stack[-1], s[i]):
                        stack.append(s[i])
                        break
                    else:
                        postfix_expression.append(stack.pop())
    while stack:
        postfix_expression.append(stack.pop())
    while len(postfix_expression) != 1:
        tmp = None
        for i in range(len(postfix_expression)):
            if postfix_expression[i] in '+-*/':
                if postfix_expression[i] == '+':
                    tmp = str(float(postfix_expression[i-2]) + float(postfix_expression[i-1]))
                elif postfix_expression[i] == '-':
                    tmp = str(float(postfix_expression[i-2]) - float(postfix_expression[i-1]))
                elif postfix_expression[i] == '*':
                    tmp = str(float(postfix_expression[i-2]) * float(postfix_expression[i-1]))
                elif postfix_expression[i] == '/':
                    tmp = str(float(postfix_expression[i-2]) / float(postfix_expression[i-1]))
                postfix_expression = postfix_expression[:i-2] + [tmp] + postfix_expression[i+1:]
                break
    print('#' + str(t+1), str(postfix_expression[0].split('.')[0]))
def right(p):
    tmp = list()
    result = True
    for i in range(len(p)):
        if p[i] == '(':
            tmp.append('(')
        else:
            if i == 0:
                result = False
                break
            if len(tmp) != 0 and tmp[-1] == '(':
                tmp.pop()
            else:
                result = False
                break
    return result

def balance(p):
    u, v = '', ''
    right, left = 0, 0
    for i in range(len(p)):
        if p[i] == '(':
            right += 1
        else:
            left += 1
        if right == left:
            u = ''.join([p[j] for j in range(i+1)])
            v = ''.join([p[j] for j in range(i+1, len(p))])
            break
    return u, v

def solve(p):
    if len(p) == 0:
        return ''
    if right(p):
        return p
    u, v = balance(p)
    if right(u):
        return u + solve(v)
    else:
        tmp = '('
        tmp += solve(v)
        tmp += ')'
        for c in u[1:len(u)-1]:
            if c == '(':
                tmp += ')'
            else:
                tmp += '('
        return ''.join(tmp)

def solution(p):
    answer = solve(p)
    return answer
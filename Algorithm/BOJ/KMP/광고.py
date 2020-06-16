def getPartialMatch(p):
    m = len(p)
    pi = [0]*m
    begin, matched = 1, 0
    while begin+matched < m:
        if p[begin+matched] == p[matched]:
            matched += 1
            pi[begin+matched-1] = matched
        else:
            if matched == 0:
                begin += 1
            else:
                begin += (matched - pi[matched-1])
                matched = pi[matched-1]
    return pi

l, p = int(input()), input()
answer = l - getPartialMatch(p)[-1]
print(answer)
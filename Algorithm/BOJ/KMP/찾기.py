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

def KMP(t, p):
    ret = []
    n, m = len(t), len(p)
    pi = getPartialMatch(p)
    begin, matched = 0, 0
    while begin <= n-m:
        if matched < m and t[begin+matched] == p[matched]:
            matched += 1
            if matched == m:
                ret.append(begin)
        else:
            if matched == 0:
                begin += 1
            else:
                begin += (matched - pi[matched-1])
                matched = pi[matched-1]
    return ret

t, p = input(), input()
answer = KMP(t, p)
print(len(answer))
for v in answer:
    print(v+1)
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

input();n = 360000
t, p = ['0']*n, ['0']*n
for idx in list(map(int, input().split())):
    t[idx-1] = '1'
for idx in list(map(int, input().split())):
    p[idx-1] = '1'
t, p = ''.join(t), ''.join(p)
t = str(t*2)[:n*2-1]
if KMP(t, p):
    print('possible')
else:
    print('impossible')
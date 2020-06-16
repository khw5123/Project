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

def gcd(a, b):
    a, b = int(a) if int(a) > int(b) else int(b), int(a) if int(a) < int(b) else int(b)
    while b != 0:
        a, b = b, a % b
    return a

n = int(input())
p = ''.join(list(map(str, input().split())))
t = (''.join(list(map(str, input().split()))))*2
t = t[:len(t)-1]
a, b = len(KMP(t, p)), n
print(str(a//gcd(a, b)) + '/' + str(b//gcd(a, b)))
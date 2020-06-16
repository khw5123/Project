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

while True:
    s = input()
    if s == '.':
        break
    answer = 1
    if not (len(s) % (len(s)-getPartialMatch(s)[-1])):
        answer = len(s) // (len(s)-getPartialMatch(s)[-1])
    print(answer)
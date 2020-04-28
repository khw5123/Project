def getPartialMatch(N):
    m = len(N)
    pi = [0] * m
    begin, matched = 1, 0
    while begin + matched < m:
        if N[begin + matched] == N[matched]:
            matched += 1
            pi[begin + matched - 1] = matched
        else:
            if matched == 0:
                begin += 1
            else:
                begin += matched - pi[matched - 1]
                matched = pi[matched - 1]
    return pi

def KMP(H, N):
    n, m = len(H), len(N)
    ret = list()
    pi = getPartialMatch(N)
    begin, matched = 0, 0
    while begin <= n - m:
        if matched < m and H[begin + matched] == N[matched]:
            matched += 1
            if matched == m:
                ret.append(begin)
        else:
            if matched == 0:
                begin += 1
            else:
                begin += matched - pi[matched - 1]
                matched = pi[matched - 1]
    return ret

def solution(phone_book):
    answer = True
    phone_book.sort(key=lambda x:len(x), reverse=True)
    phone_book.sort(key=lambda x:x[0])
    for i in range(len(phone_book)-1):
        for j in range(i+1, len(phone_book)):
            tmp = KMP(phone_book[i], phone_book[j])
            if len(tmp) != 0 and tmp[0] == 0:
                return False
    return answer
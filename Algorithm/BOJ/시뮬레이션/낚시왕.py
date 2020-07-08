import sys
input = sys.stdin.readline

def calcPosition(n, m, r, c, s, d):
    if d == 1:
        if r-1 < s:
            s -= r-1
            d, r = 2, 1
            while n-1 < s:
                s -= n-1
                if d == 2:
                    d, r = 1, n
                else:
                    d, r = 2, 1
            if d == 2:
                r = 1+s
            else:
                r = n-s
        else:
            r -= s
    elif d == 2:
        if n-r < s:
            s -= n-r
            d, r = 1, n
            while n-1 < s:
                s -= n-1
                if d == 1:
                    d, r = 2, 1
                else:
                    d, r = 1, n
            if d == 1:
                r = n-s
            else:
                r = 1+s
        else:
            r += s
    elif d == 3:
        if m-c < s:
            s -= m-c
            d, c = 4, m
            while m-1 < s:
                s -= m-1
                if d == 4:
                    d, c = 3, 1
                else:
                    d, c = 4, m
            if d == 4:
                c = m-s
            else:
                c = 1+s
        else:
            c += s
    else:
        if c-1 < s:
            s -= c-1
            d, c = 3, 1
            while m-1 < s:
                s -= m-1
                if d == 3:
                    d, c = 4, m
                else:
                    d, c = 3, 1
            if d == 3:
                c = 1+s
            else:
                c = m-s
        else:
            c -= s
    return r, c, d

n, m, k = map(int, input().split())
shark, answer = dict(), 0
for _ in range(k):
    r, c, s, d, z = map(int, input().split())
    shark[(r, c)] = [s, d, z]
for i in range(1, m+1):
    change, catch = dict(), (101, 101)
    for k, v in shark.items():
        r, c, s, d, z = k[0], k[1], v[0], v[1], v[2]
        if i != 1:
            r, c, d = calcPosition(n, m, r, c, s, d)
        if (r, c) in change:
            if change[(r, c)][2] < z:
                change[(r, c)] = [s, d, z]
        else:
            change[(r, c)] = [s, d, z]
        if c == i and catch[0] > r:
            catch = (r, c)
    if catch in change:
        answer += change[catch][2]
        change.pop(catch)
    shark = change
print(answer)
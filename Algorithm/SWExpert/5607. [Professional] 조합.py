mod = 1234567891

def solve(n, x):
    global mod
    if x == 0:
        return 1
    num = solve(n, x//2)
    ret = (num * num) % mod
    if x % 2 == 0:
        return ret
    else:
        return (ret * n) % mod

for t in range(int(input())):
    n, r = map(int, input().split())
    factorial = [1]*(n+1)
    for i in range(1, n+1):
        factorial[i] = (factorial[i-1] * i) % mod
    denominator = solve((factorial[r] * factorial[n-r]) % mod, mod-2)
    answer = (factorial[n] * denominator) % mod
    print('#' + str(t+1), str(answer))
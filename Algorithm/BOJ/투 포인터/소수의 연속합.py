def sieveOfEratosthenes(n):
    sieve = [True]*n
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*2, n, i):
                sieve[j] = False
    return [i for i in range(2, n) if sieve[i]]

n = int(input())
arr = sieveOfEratosthenes(n+1)
answer, _sum, end = 0, 0, 0
for start in range(len(arr)):
    while _sum < n and end < len(arr):
        _sum += arr[end]
        end += 1
    if _sum == n:
        answer += 1
    _sum -= arr[start]
print(answer)
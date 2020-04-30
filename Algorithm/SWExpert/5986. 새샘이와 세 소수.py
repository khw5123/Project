def sieve_of_eratosthenes(n):
    arr = [True] * n
    for i in range(2, int(n**0.5) + 1):
        if arr[i] == True:
            for j in range(i*2, n, i):
                arr[j] = False
    return [i for i in range(2, n) if arr[i] == True]

for t in range(int(input())):
    n = int(input())
    prime = sieve_of_eratosthenes(n)
    answer = 0
    for i in range(len(prime)):
        for j in range(i, len(prime)):
            if n - (prime[i] + prime[j]) in prime[j:]:
                answer += 1
    print('#' + str(t+1), answer)
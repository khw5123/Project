def sieve_of_eratosthenes(n):
    arr = [True]*n
    for i in range(2, int(n**0.5)+1):
        if arr[i] == True:
            for j in range(i*2, n, i):
                arr[j] = False
    return [i for i in range(2, n) if arr[i] == True]

prime = sieve_of_eratosthenes(1000000)

for t in range(int(input())):
    d, a, b = map(int, input().split())
    answer = 0
    for n in prime:
        if n > b:
            break
        if n >= a and str(d) in str(n):
            answer += 1
    print('#' + str(t+1), str(answer))
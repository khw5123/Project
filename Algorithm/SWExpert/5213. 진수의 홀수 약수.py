def solve(n):
    result = [0]*(n+1)
    for i in range(1, n+1, 2):
        j = 1
        while i*j < n+1:
            result[i*j] += i
            j += 1
    for i in range(1, n+1):
        result[i] += result[i-1]
    return result

li = solve(pow(10,6))

for t in range(int(input())):
    a, b = map(int, input().split())
    print('#' + str(t+1), str(li[b]-li[a-1]))
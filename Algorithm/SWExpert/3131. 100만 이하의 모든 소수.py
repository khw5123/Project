import math

def solve(n):
    arr = [True]*(n+1)
    for i in range(2, int(math.sqrt(n+1) + 1)):
        if arr[i] == True:
            for j in range(i*2, n+1, i):
                arr[j] = False
    return [i for i in range(2, n+1) if arr[i] == True]

for i in solve(pow(10, 6)):
    print(i, end=' ')
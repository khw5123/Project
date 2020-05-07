for t in range(int(input())):
    n, m = map(int, input().split())
    restrict = set()
    answer = 0
    for _ in range(m):
        a, b = map(int, input().split())
        restrict.add(pow(2, a-1) + pow(2, b-1))
    for bit in range(pow(2, n)):
        answer += 1
        for restrict_bit in restrict:
            if bit | restrict_bit == bit:
                answer -= 1
                break
    print('#' + str(t+1), answer)

'''
from itertools import combinations

for t in range(int(input())):
    n, m = map(int, input().split())
    answer = []
    for count in range(n+1):
        answer += list(combinations([i for i in range(1, n+1)], count))
    answer = set(answer)
    for _ in range(m):
        a, b = map(int, input().split())
        comb = []
        for count in range(n+1):
            comb += list(combinations([i for i in range(1, n+1) if i != a], count))
            comb += list(combinations([i for i in range(1, n+1) if i != b], count))
        answer &= set(comb)
    print('#' + str(t+1), len(answer))
'''
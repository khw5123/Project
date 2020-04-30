def update(index, value):
    while index <= n:
        bit[index] += value
        index += (index & (-index))

def add(index):
    sum_ = 0
    while index > 0:
        sum_ += bit[index]
        index -= (index & (-index))
    return sum_

for t in range(int(input())):
    n, m = map(int, input().split())
    li = [0] + list(map(int, input().split()))
    bit = [0]*(n+1)
    answer = []
    for i in range(1, n+1):
        update(i, li[i])
    for _ in range(m):
        a, b, c = map(int, input().split())
        if a == 1:
            update(b, c)
        else:
            answer.append(add(c) - add(b-1))
    print('#' + str(t+1), end=' ')
    for v in answer:
        print(v, end=' ')
    print()
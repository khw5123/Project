def solve():
    current, connected = [s], [s]
    while True:
        tmp, next_connect = [], []
        for next_idx in current:
            tmp.extend(li[next_idx])
        for v in tmp:
            if v not in connected:
                next_connect.append(v)
        if not len(next_connect):
            break
        current = next_connect
        connected += tmp
    return max(current)

for t in range(10):
    n, s = map(int, input().split())
    li = [[] for _ in range(n+1)]
    tmp = list(map(int, input().split()))
    for i in range(0, len(tmp), 2):
        li[tmp[i]].append(tmp[i+1])
    answer = solve()
    print('#' + str(t+1), str(answer))
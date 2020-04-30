for t in range(int(input())):
    a, b = map(int, input().split())
    x, y = [1, 0], [0, 1]
    r, q = [a, b], [0]
    idx = 1
    while r[-1] != 0:
        q.append(r[idx-1]//r[idx])
        idx += 1
        r.append(r[idx-2] % r[idx-1])
        x.append(x[idx-2] - x[idx-1]*q[idx-1])
        y.append(y[idx-2] - y[idx-1]*q[idx-1])
    print('#' + str(t+1), str(x[-2]), str(y[-2]))
for t in range(int(input())):
    p, q, r, s, w = map(int, input().split())
    a, b = p*w, q
    if w > r:
        b += s*(w-r)
    if a > b:
        print('#' + str(t+1) + ' ' + str(b))
    else:
        print('#' + str(t+1) + ' ' + str(a))
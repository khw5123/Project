for t in range(int(input())):
    h1, m1, h2, m2 = map(int, input().split())
    if m1 + m2 >= 60:
        h = h1 + h2 + (m1 + m2) // 60
        if h > 12:
            h -= 12
        m = (m1 + m2) % 60
    else:
        h = h1 + h2
        if h > 12:
            h -= 12
        m = m1 + m2
    print('#' + str(t+1) + ' ' + str(h) + ' ' + str(m))
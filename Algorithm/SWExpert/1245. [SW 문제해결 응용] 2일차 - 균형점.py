for t in range(int(input())):
    n = int(input())
    li, save = list(map(int, input().split())), []
    answer = []
    for i in range(n):
        save.append([li[i], li[i+n]])
    save.sort()
    for i in range(n-1):
        l, r = save[i][0], save[i+1][0]
        count = 0
        while count < 100:
            m = (l+r)/2
            f_l, f_r = 0., 0.
            for x_, m_ in save:
                if x_ != m:
                    if x_ < m:
                        f_l += m_/pow(m-x_, 2)
                    else:
                        f_r += m_/pow(x_-m, 2)
            f = f_r-f_l
            if f < 0:
                l = m
            elif f > 0:
                r = m
            else:
                break
            count += 1
        answer.append(m)
    print('#' + str(t+1), end=' ')
    for v in answer:
        print('%.10f' % v, end=' ')
    print()

'''
for t in range(int(input())):
    n = int(input())
    li = list(map(int, input().split()))
    save = [[li[i], '+'] for i in range(n-1)]
    answer = ['']*(n-1)
    for k in range(n-1):
        distance = 987654321
        for x in range(li[k], li[k+1]+1):
            if x not in li[:n]:
                l, r = 0., 0.
                for i in range(n):
                    x_, m_ = li[i], li[i+n]
                    if x_ < x:
                        l += m_/pow(x-x_, 2)
                    elif x_ > x:
                        r += m_/pow(x_-x, 2)
                if distance > abs(l-r):
                    distance = abs(l-r)
                    save[k][0], save[k][1] = x, ('-' if l-r < 0 else '+')
    idx = 0
    for start, direction in save:
        if direction == '-':
            start -= 1
        distance, count, exit_ = 987654321, 0, 0
        x = str(start) + '.'
        d = [distance]
        while count != 10 and exit_ < 2:
            length = len(x)
            for i in range(10):
                sub_x = x + str(i)
                if float(sub_x) not in li[:n]:
                    l, r = 0., 0.
                    for i in range(n):
                        x_, m_ = li[i], li[i+n]
                        if x_ < float(sub_x):
                            l += m_/pow(float(sub_x)-x_, 2)
                        elif x_ > float(sub_x):
                            r += m_/pow(x_-float(sub_x), 2)
                    if distance > abs(l-r):
                        distance = abs(l-r)
                        d.append(distance)
                        answer[idx] = sub_x
            if distance == 0:
                break
            x = answer[idx]
            if length == len(x):
                confirm = True
                sub_x = x + ''.join(['0' for _ in range(9-count)]) + '1'
                l, r = 0., 0.
                for i in range(n):
                    x_, m_ = li[i], li[i+n]
                    if x_ < float(sub_x):
                        l += m_/pow(float(sub_x)-x_, 2)
                    elif x_ > float(sub_x):
                        r += m_/pow(x_-float(sub_x), 2)
                if distance > abs(l-r):
                    confirm = False
                if confirm:
                    x = x[:len(x)-1] + str(int(x[-1])-1)
                    exit_ += 1
                    d.pop()
                    distance = d[-1]
                    continue
                else:
                    x += '0'
                    answer[idx] = x
            exit_ = 0
            count += 1
        idx += 1
    print('#' + str(t+1), end=' ')
    for v in answer:
        print('%.10f' % float(v), end=' ')
    print()
'''
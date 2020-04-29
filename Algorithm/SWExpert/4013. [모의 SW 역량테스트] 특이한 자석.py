import copy

def turn(arr, direction):
    if direction == 1:
        tmp = copy.deepcopy(arr)
        for i in range(len(arr)-1):
            tmp[i+1] = arr[i]
        tmp[0] = arr[-1]
        return tmp
    else:
        tmp = copy.deepcopy(arr)
        for i in range(len(arr)-1):
            tmp[i] = arr[i+1]
        tmp[-1] = arr[0]
        return tmp

for t in range(int(input())):
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))
    d = list(map(int, input().split()))
    for i in range(n):
        k, direction = map(int, input().split())
        if k == 1:
            if direction == 1:
                if a[2] != b[6]:
                    if b[2] != c[6]:
                        if c[2] != d[6]:
                            d = turn(d, -1)
                        c = turn(c, 1)
                    b = turn(b, -1)
                a = turn(a, 1)
            else:
                if a[2] != b[6]:
                    if b[2] != c[6]:
                        if c[2] != d[6]:
                            d = turn(d, 1)
                        c = turn(c, -1)
                    b = turn(b, 1)
                a = turn(a, -1)
        elif k == 2:
            if direction == 1:
                if a[2] != b[6]:
                    a = turn(a, -1)
                if b[2] != c[6]:
                    if c[2] != d[6]:
                        d = turn(d, 1)
                    c = turn(c, -1)
                b = turn(b, 1)
            else:
                if a[2] != b[6]:
                    a = turn(a, 1)
                if b[2] != c[6]:
                    if c[2] != d[6]:
                        d = turn(d, -1)
                    c = turn(c, 1)
                b = turn(b, -1)
        elif k == 3:
            if direction == 1:
                if c[2] != d[6]:
                    d = turn(d, -1)
                if b[2] != c[6]:
                    if a[2] != b[6]:
                        a = turn(a, 1)
                    b = turn(b, -1)
                c = turn(c, 1)
            else:
                if c[2] != d[6]:
                    d = turn(d, 1)
                if b[2] != c[6]:
                    if a[2] != b[6]:
                        a = turn(a, -1)
                    b = turn(b, 1)
                c = turn(c, -1)
        elif k == 4:
            if direction == 1:
                if c[2] != d[6]:
                    if b[2] != c[6]:
                        if a[2] != b[6]:
                            a = turn(a, -1)
                        b = turn(b, 1)
                    c = turn(c, -1)
                d = turn(d, 1)
            else:
                if c[2] != d[6]:
                    if b[2] != c[6]:
                        if a[2] != b[6]:
                            a = turn(a, 1)
                        b = turn(b, -1)
                    c = turn(c, 1)
                d = turn(d, -1)
    answer = a[0] + b[0] * 2 + c[0] * 4 + d[0] * 8
    print('#' + str(t+1), str(answer))
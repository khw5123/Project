def find(a):
    global li
    if a == li[a]:
        return a
    else:
        li[a] = find(li[a])
        return li[a]

def union(a, b):
    global li
    li[find(a)] = find(b)

for t in range(int(input())):
    n, m = map(int, input().split())
    li = [i for i in range(1000001)]
    answer = ''
    for _ in range(m):
        k, a, b = map(int, input().split())
        if k == 0:
            union(a, b)
        else:
            if find(a) == find(b):
                answer += '1'
            else:
                answer += '0'
    print('#' + str(t+1) + ' ' + answer)
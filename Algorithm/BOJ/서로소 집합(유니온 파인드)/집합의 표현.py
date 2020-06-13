import sys
input = sys.stdin.readline

def find(a):
    if a == li[a]:
        return a
    else:
        li[a] = find(li[a])
        return li[a]

def union(a, b):
    li[find(a)] = find(b)

n, m = map(int, input().split())
li = [i for i in range(n+1)]
for _ in range(m):
    k, a, b = map(int, input().split())
    if k == 0:
        union(a, b)
    else:
        if find(a) == find(b):
            print('YES')
        else:
            print('NO')
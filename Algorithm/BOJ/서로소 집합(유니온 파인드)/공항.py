import sys
input = sys.stdin.readline

def find(a):
    if a == li[a]:
        return a
    li[a] = find(li[a])
    return li[a]

def union(a, b):
    li[find(a)] = find(b)

g, p = int(input()), int(input())
li = [i for i in range(g+1)]
answer = 0
for _ in range(p):
    gi = int(input())
    ret = find(gi)
    if ret == 0:
        break
    union(ret, ret-1)
    answer += 1
print(answer)
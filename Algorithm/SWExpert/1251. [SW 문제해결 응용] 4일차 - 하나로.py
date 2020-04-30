import math

def find(a):
    if a == li[a]:
        return a
    else:
        li[a] = find(li[a])
        return li[a]

def union(a, b):
    a, b = find(a), find(b)
    if a == b:
        return False
    else:
        li[a] = b
        return True

for t in range(int(input())):
    n = int(input())
    li = [i for i in range(n+1)]
    coord = []
    for x in list(map(int, input().split())):
        coord.append([x])
    tmp = list(map(int, input().split()))
    for i in range(len(tmp)):
        coord[i].append(tmp[i])
    e = float(input())
    edge = []
    for i in range(n):
        for j in range(i+1, n):
            edge.append([i, j, math.sqrt(pow(coord[i-1][0] - coord[j-1][0], 2) + pow(coord[i-1][1] - coord[j-1][1], 2))])
    edge.sort(key=lambda x:x[2])
    answer = 0.
    for i in range(len(edge)):
        if union(edge[i][0], edge[i][1]):
            answer += e*edge[i][2]*edge[i][2]
    print('#' + str(t+1), str(round(answer)))
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
    v, e = map(int, input().split())
    li = [i for i in range(v+1)]
    edge = []
    answer = 0
    for _ in range(e):
        a, b, c = map(int, input().split())
        edge.append([a, b, c])
    edge.sort(key=lambda x:x[2])
    for i in range(len(edge)):
        if union(edge[i][0], edge[i][1]):
            answer += edge[i][2]
    print('#' + str(t+1), str(answer))
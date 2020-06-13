def find(a):
    if a == li[a]:
        return a
    li[a] = find(li[a])
    return li[a]

def union(a, b):
    a, b = find(a), find(b)
    if a != b:
        li[a] = b

n = int(input())
m = int(input())
li = [i for i in range(n+1)]
city = []
answer = 'YES'
for _ in range(n):
    city.append(list(map(int, input().split())))
for i in range(n-1):
    for j in range(i+1, n):
        if city[i][j] == 1:
            union(i+1, j+1)
path = list(map(int, input().split()))
for i in range(m-1):
    if find(path[i]) != find(path[i+1]):
        answer = 'NO'
        break
print(answer)
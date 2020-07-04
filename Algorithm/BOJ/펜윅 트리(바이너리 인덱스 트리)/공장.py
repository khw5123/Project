import sys
input = sys.stdin.readline

def update(tree, index):
    while index <= n:
        tree[index] += 1
        index += (index & (-index))

def _sum(tree, index):
    result = 0
    while index > 0:
        result += tree[index]
        index -= (index & (-index))
    return result

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
tree, index = [0]*(n+1), [0]*(n+1)
tmp = [0]*(max(a)+1)
answer = 0
for i in range(n):
    tmp[b[i]] = i+1
for i in range(n):
    index[i+1] = tmp[a[i]]
for i in range(1, n+1):
    answer += _sum(tree, n) - _sum(tree, index[i])
    update(tree, index[i])
print(answer)
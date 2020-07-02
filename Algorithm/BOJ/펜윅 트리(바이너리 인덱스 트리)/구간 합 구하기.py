import sys
input = sys.stdin.readline

def update(tree, index, diff):
    while index < len(tree):
        tree[index] += diff
        index += (index & (-index))

def _sum(tree, index):
    result = 0
    while index > 0:
        result += tree[index]
        index -= (index & (-index))
    return result

n, m, k = map(int, input().split())
arr, tree = [0]*(n+1), [0]*(n+1)
for i in range(1, n+1):
    arr[i] = int(input())
    update(tree, i, arr[i])
for _ in range(m+k):
    a, b, c = map(int, input().split())
    if a == 1:
        update(tree, b, c-arr[b])
        arr[b] = c
    else:
        print(_sum(tree, c) - _sum(tree, b-1))
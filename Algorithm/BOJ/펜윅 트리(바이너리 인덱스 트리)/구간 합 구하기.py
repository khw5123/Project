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
'''
import sys
import math
input = sys.stdin.readline

def init(arr, tree, node, start, end):
    if start == end:
        tree[node] = arr[start]
        return tree[node]
    mid = (start+end) // 2
    tree[node] = init(arr, tree, node*2, start, mid) + init(arr, tree, node*2+1, mid+1, end)
    return tree[node]

def update(tree, node, start, end, index, diff):
    if not (start <= index and index <= end):
        return
    tree[node] += diff
    if start != end:
        mid = (start+end) // 2
        update(tree, node*2, start, mid, index, diff)
        update(tree, node*2+1, mid+1, end, index, diff)

def _sum(tree, node, start, end, left, right):
    if left > end or right < start:
        return 0
    if left <= start and end <= right:
        return tree[node]
    mid = (start+end) // 2
    return _sum(tree, node*2, start, mid, left, right) + _sum(tree, node*2+1, mid+1, end, left, right)

n, m, k = map(int, input().split())
arr, tree = [], [0]*(1 << (int(math.ceil(math.log2(n)))+1))
for _ in range(n):
    arr.append(int(input()))
init(arr, tree, 1, 0, n-1)
for _ in range(m+k):
    a, b, c = map(int, input().split())
    if a == 1:
        update(tree, 1, 0, n-1, b-1, c-arr[b-1])
        arr[b-1] = c
    else:
        print(_sum(tree, 1, 0, n-1, b-1, c-1))
'''
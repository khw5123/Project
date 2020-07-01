import sys
input = sys.stdin.readline

def update(tree, index, diff):
    while index < len(tree):
        tree[index] = min(tree[index], diff)
        index += (index & (-index))

def update2(tree, index, diff):
    while index > 0:
        tree[index] = min(tree[index], diff)
        index -= (index & (-index))

def query(a, b):
    ret = MAX
    prev = a
    curr = prev + (prev & -prev)
    while curr <= b:
        ret = min(ret, tree2[prev])
        prev = curr
        curr = prev + (prev & -prev)
    ret = min(ret, arr[prev])
    prev = b
    curr = prev - (prev & -prev)
    while curr >= a:
        ret = min(ret, tree[prev])
        prev = curr
        curr = prev - (prev & -prev)
    return ret

n, m = map(int, input().split())
arr, MAX = [0]*(n+1), 1000000001
tree, tree2 = [MAX]*(n+2), [MAX]*(n+2)
for i in range(1, n+1):
    arr[i]= int(input())
    update(tree, i, arr[i])
    update2(tree2, i, arr[i])
for _ in range(m):
    a, b = map(int, input().split())
    print(query(a, b))
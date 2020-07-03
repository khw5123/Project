import sys
import math
input = sys.stdin.readline

def init(tree, arr, node, nodeL, nodeR, _type):
    if nodeL == nodeR: # 단말 노드일 경우
        tree[node] = arr[nodeL] # 단말 노드에 값 저장
        return tree[node]
    mid = (nodeL+nodeR)//2
    if _type == 'min':
        tree[node] = min(init(tree, arr, node*2, nodeL, mid, _type), init(tree, arr, node*2+1, mid+1, nodeR, _type))
    else:
        tree[node] = max(init(tree, arr, node*2, nodeL, mid, _type), init(tree, arr, node*2+1, mid+1, nodeR, _type))
    return tree[node]

def query(treeMin, treeMax, l, r, node, nodeL, nodeR, _type):
    if r < nodeL or nodeR < l: # 구간이 겹치지 않는 경우
        if _type == 'min':
            return MAX+1
        else:
            return MIN-1
    if l <= nodeL and nodeR <= r: # 구간이 완전히 포함되는 경우
        if _type == 'min':
            return treeMin[node]
        else:
            return treeMax[node]
    mid = (nodeL+nodeR)//2
    if _type == 'min':
        return min(query(treeMin, treeMax, l, r, node*2, nodeL, mid, _type), query(treeMin, treeMax, l, r, node*2+1, mid+1, nodeR, _type))
    else:
        return max(query(treeMin, treeMax, l, r, node*2, nodeL, mid, _type), query(treeMin, treeMax, l, r, node*2+1, mid+1, nodeR, _type))

n, m = map(int, input().split())
arr, MIN, MAX = [0]*(n+1), 1, 1000000000
treeMin = [0]*(1 << (int(math.ceil(math.log2(n)))+1))
treeMax = [0]*(1 << (int(math.ceil(math.log2(n)))+1))
for i in range(1, n+1):
    arr[i] = int(input())
init(treeMin, arr, 1, 1, n, 'min') # 세그먼트 트리 생성
init(treeMax, arr, 1, 1, n, 'max') # 세그먼트 트리 생성
for _ in range(m):
    a, b = map(int, input().split())
    print(query(treeMin, treeMax, a, b, 1, 1, n, 'min'), end=' ')
    print(query(treeMin, treeMax, a, b, 1, 1, n, 'max'))
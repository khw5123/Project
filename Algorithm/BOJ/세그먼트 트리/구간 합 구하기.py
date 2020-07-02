# 값 변경 시 현재 값과 변경될 값의 차이를 구해서 루트 노드부터 단말 노드까지 값을 갱신하는 경우
import sys
import math
input = sys.stdin.readline

def init(tree, arr, node, nodeL, nodeR):
    if nodeL == nodeR: # 단말 노드일 경우
        tree[node] = arr[nodeL] # 단말 노드에 값 저장
        return tree[node]
    mid = (nodeL+nodeR)//2
    tree[node] = init(tree, arr, node*2, nodeL, mid) + init(tree, arr, node*2+1, mid+1, nodeR)
    return tree[node]

def update(tree, target, diff, node, nodeL, nodeR):
    if not (nodeL <= target and target <= nodeR): # 값을 변경할 노드가 구간에 있을 경우
        return
    tree[node] += diff # 내부 or 단말 노드의 값에 차이값 만큼 추가
    if nodeL != nodeR: # 단말 노드가 아닐 경우
        mid = (nodeL+nodeR)//2
        update(tree, target, diff, node*2, nodeL, mid)
        update(tree, target, diff, node*2+1, mid+1, nodeR)

def _sum(tree, l, r, node, nodeL, nodeR):
    if r < nodeL or nodeR < l: # 구간이 겹치지 않는 경우
        return 0
    if l <= nodeL and nodeR <= r: # 구간이 완전히 포함되는 경우
        return tree[node]
    mid = (nodeL+nodeR)//2
    return _sum(tree, l, r, node*2, nodeL, mid) + _sum(tree, l, r, node*2+1, mid+1, nodeR)

n, m, k = map(int, input().split())
arr, tree = [0]*(n+1), [0]*(1 << (int(math.ceil(math.log2(n)))+1))
for i in range(1, n+1):
    arr[i] = int(input())
init(tree, arr, 1, 1, n) # 세그먼트 트리 생성
for _ in range(m+k):
    a, b, c = map(int, input().split())
    if a == 1:
        update(tree, b, c-arr[b], 1, 1, n)
        arr[b] = c
    else:
        print(_sum(tree, b, c, 1, 1, n))
'''
# 단말 노드의 위치를 저장해두고 값 변경 시 단말 노드부터 루트 노드까지 값을 갱신하는 경우
import sys
import math
input = sys.stdin.readline

def init(tree, arr, leaf, node, nodeL, nodeR):
    if nodeL == nodeR: # 단말 노드일 경우
        tree[node] = arr[nodeL] # 단말 노드에 값 저장
        leaf[nodeL] = node # 단말 노드의 인덱스 저장
        return tree[node]
    mid = (nodeL+nodeR)//2
    tree[node] = init(tree, arr, leaf, node*2, nodeL, mid) + init(tree, arr, leaf, node*2+1, mid+1, nodeR)
    return tree[node]

def update(tree, leaf, node, val):
    index = leaf[node] # 단말 노드의 위치(단말 노드의 인덱스) 저장
    tree[index] = val # 값 변경
    while index > 1:
        index //= 2
        tree[index] = tree[index*2] + tree[index*2+1] # 내부 노드의 값 변경

def _sum(tree, l, r, node, nodeL, nodeR):
    if r < nodeL or nodeR < l: # 구간이 겹치지 않는 경우
        return 0
    if l <= nodeL and nodeR <= r: # 구간이 완전히 포함되는 경우
        return tree[node]
    mid = (nodeL+nodeR)//2
    return _sum(tree, l, r, node*2, nodeL, mid) + _sum(tree, l, r, node*2+1, mid+1, nodeR)

n, m, k = map(int, input().split())
arr, tree = [0]*(n+1), [0]*(1 << (int(math.ceil(math.log2(n)))+1))
leaf = dict() # 단말 노드의 인덱스(leaf[단말 노드 번호] = 단말 노드의 인덱스)
for i in range(1, n+1):
    arr[i] = int(input())
init(tree, arr, leaf, 1, 1, n) # 세그먼트 트리 생성
for _ in range(m+k):
    a, b, c = map(int, input().split())
    if a == 1:
        update(tree, leaf, b, c)
    else:
        print(_sum(tree, b, c, 1, 1, n))
'''
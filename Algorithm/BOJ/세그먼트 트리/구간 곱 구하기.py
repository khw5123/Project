import sys
import math
input = sys.stdin.readline

def init(tree, arr, leaf, node, nodeL, nodeR):
    if nodeL == nodeR: # 단말 노드일 경우
        tree[node] = arr[nodeL] # 단말 노드에 값 저장
        leaf[nodeL] = node # 단말 노드의 인덱스 저장
        return tree[node]
    mid = (nodeL+nodeR)//2
    tree[node] = (init(tree, arr, leaf, node*2, nodeL, mid) * init(tree, arr, leaf, node*2+1, mid+1, nodeR)) % 1000000007
    return tree[node]

def update(tree, leaf, node, val):
    index = leaf[node] # 단말 노드의 위치(단말 노드의 인덱스) 저장
    tree[index] = val # 값 변경
    while index > 1:
        index //= 2
        tree[index] = (tree[index*2] * tree[index*2+1]) % 1000000007 # 내부 노드의 값 변경

def mul(tree, l, r, node, nodeL, nodeR):
    if r < nodeL or nodeR < l: # 구간이 겹치지 않는 경우
        return 1
    if l <= nodeL and nodeR <= r: # 구간이 완전히 포함되는 경우
        return tree[node]
    mid = (nodeL+nodeR)//2
    return (mul(tree, l, r, node*2, nodeL, mid) * mul(tree, l, r, node*2+1, mid+1, nodeR)) % 1000000007

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
        arr[b] = c
    else:
        print(mul(tree, b, c, 1, 1, n))
import sys
import math
input = sys.stdin.readline

def init(tree, arr, node, nodeL, nodeR):
    if nodeL == nodeR: # 단말 노드일 경우
        tree[node] = arr[nodeL] # 단말 노드에 값 저장
        return tree[node]
    mid = (nodeL+nodeR)//2
    tree[node] = min(init(tree, arr, node*2, nodeL, mid), init(tree, arr, node*2+1, mid+1, nodeR))
    return tree[node]

def _min(tree, l, r, node, nodeL, nodeR):
    if r < nodeL or nodeR < l: # 구간이 겹치지 않는 경우
        return MAX+1
    if l <= nodeL and nodeR <= r: # 구간이 완전히 포함되는 경우
        return tree[node]
    mid = (nodeL+nodeR)//2
    return min(_min(tree, l, r, node*2, nodeL, mid), _min(tree, l, r, node*2+1, mid+1, nodeR))

n, m = map(int, input().split())
arr, MAX = [0]*(n+1), 1000000000
tree = [0]*(1 << (int(math.ceil(math.log2(n)))+1))
for i in range(1, n+1):
    arr[i] = int(input())
init(tree, arr, 1, 1, n) # 세그먼트 트리 생성
for _ in range(m):
    a, b = map(int, input().split())
    print(_min(tree, a, b, 1, 1, n))
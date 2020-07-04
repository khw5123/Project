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

n, q = map(int, input().split())
arr = [0] + list(map(int, input().split()))
tree = [0]*(1 << (int(math.ceil(math.log2(n)))+1))
init(tree, arr, 1, 1, n) # 세그먼트 트리 생성
for _ in range(q):
    x, y, a, b = map(int, input().split())
    if x > y:
        x, y = y, x
    print(_sum(tree, x, y, 1, 1, n))
    update(tree, a, b-arr[a], 1, 1, n)
    arr[a] = b
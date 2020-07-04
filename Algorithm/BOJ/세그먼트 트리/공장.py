import sys
import math
input = sys.stdin.readline

def update(tree, target, node, nodeL, nodeR):
    if not (nodeL <= target and target <= nodeR): # 값을 변경할 노드가 구간에 있을 경우
        return
    tree[node] += 1 # 내부 or 단말 노드의 값에 차이값 만큼 추가
    if nodeL != nodeR: # 단말 노드가 아닐 경우
        mid = (nodeL+nodeR)//2
        update(tree, target, node*2, nodeL, mid)
        update(tree, target, node*2+1, mid+1, nodeR)

def _sum(tree, l, r, node, nodeL, nodeR):
    if r < nodeL or nodeR < l: # 구간이 겹치지 않는 경우
        return 0
    if l <= nodeL and nodeR <= r: # 구간이 완전히 포함되는 경우
        return tree[node]
    mid = (nodeL+nodeR)//2
    return _sum(tree, l, r, node*2, nodeL, mid) + _sum(tree, l, r, node*2+1, mid+1, nodeR)

n = int(input())
a, b = list(map(int, input().split())), list(map(int, input().split()))
tree, index = [0]*(1 << (int(math.ceil(math.log2(n)))+1)), [0]*(n+1)
tmp = [0]*(max(a)+1)
answer = 0
for i in range(n):
    tmp[b[i]] = i+1
for i in range(n):
    index[i+1] = tmp[a[i]]
for i in range(1, n+1):
    answer += _sum(tree, index[i], n, 1, 1, n)
    update(tree, index[i], 1, 1, n)
print(answer)
import sys
import math
sys.setrecursionlimit(10**6)
input = sys.stdin.readline

def update(tree, target, diff, node, nodeL, nodeR):
    if not (nodeL <= target and target <= nodeR): # 값을 변경할 노드가 구간에 있을 경우
        return
    tree[node] += diff # 내부 or 단말 노드의 값에 차이값 만큼 추가
    if nodeL != nodeR: # 단말 노드가 아닐 경우
        mid = (nodeL+nodeR)//2
        update(tree, target, diff, node*2, nodeL, mid)
        update(tree, target, diff, node*2+1, mid+1, nodeR)

def query(tree, b, node, nodeL, nodeR):
    if nodeL == nodeR: # 단말 노드일 경우
        return nodeL # 노드 번호(꺼낼 사탕의 맛의 번호) 반환
    mid = (nodeL+nodeR)//2
    if tree[node*2] >= b: # 왼쪽 구간에 있는 사탕 개수의 합이 꺼낼 사탕의 순위보다 크거나 같을 경우
        return query(tree, b, node*2, nodeL, mid) # 왼쪽 구간 탐색
    b -= tree[node*2] # 왼쪽 구간에 있는 사탕 개수의 합 만큼 꺼낼 사탕의 순위에서 제거
    if tree[node*2+1] >= b: # 오른쪽 구간에 있는 사탕 개수의 합이 꺼낼 사탕의 순위보다 크거나 같을 경우
        return query(tree, b, node*2+1, mid+1, nodeR) # 오른쪽 구간 탐색

n, MAX = int(input()), 1000000
tree = [0]*(1 << (int(math.ceil(math.log2(MAX)))+1)) # 처음에는 빈 사탕상자에서 시작
for _ in range(n):
    tmp = list(map(int, input().split()))
    a, b = tmp[0], tmp[1]
    if a == 1:
        target = query(tree, b, 1, 1, MAX)
        print(target) # 노드 번호(꺼낼 사탕의 맛의 번호) 출력
        update(tree, target, -1, 1, 1, MAX)
    else:
        c = tmp[2]
        update(tree, b, c, 1, 1, MAX)
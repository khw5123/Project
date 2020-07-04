import sys
import math
input = sys.stdin.readline

def init(tree, node, nodeL, nodeR):
    if nodeL == nodeR: # 단말 노드일 경우
        tree[node] = 1 # 단말 노드에 값 저장
        return tree[node]
    mid = (nodeL+nodeR)//2
    tree[node] = init(tree, node*2, nodeL, mid) + init(tree, node*2+1, mid+1, nodeR)
    return tree[node]

def query(tree, num, node, nodeL, nodeR):
    tree[node] -= 1 # 탐색 시 노드의 값을 1감소시킴
    if nodeL == nodeR: # 단말 노드일 경우
        return nodeL # 노드 번호(i번째 원소가 저장될 위치) 반환
    mid = (nodeL+nodeR)//2
    if tree[node*2] >= num: # 왼쪽 구간에 있는 원소 개수의 합이 i번째 원소 앞에 있는 수들 중 i보다 큰 수들의 개수보다 크거나 같을 경우
        return query(tree, num, node*2, nodeL, mid) # 왼쪽 구간 탐색
    num -= tree[node*2] # 왼쪽 구간에 있는 원소 개수의 합 만큼 i번째 원소 앞에 있는 수들 중 i보다 큰 수들의 개수에서 제거
    if tree[node*2+1] >= num: # 오른쪽 구간에 있는 원소 개수의 합이 i번째 원소 앞에 있는 수들 중 i보다 큰 수들의 개수보다 크거나 같을 경우
        return query(tree, num, node*2+1, mid+1, nodeR) # 오른쪽 구간 탐색

n = int(input())
answer, tree = [0]*(n+1), [0]*(1 << (int(math.ceil(math.log2(n)))+1))
init(tree, 1, 1, n) # 세그먼트 트리 생성(단말 노드를 모두 1로 초기화 = 원소 배치)
for i in range(1, n+1):
    num = int(input())
    answer[query(tree, num+1, 1, 1, n)] = i # i번째 원소가 저장될 위치(노드) 찾아서 i번째 원소 저장
for i in range(1, n+1):
    print(answer[i])
'''
import sys
import math
input = sys.stdin.readline

def init(tree, node, nodeL, nodeR):
    if nodeL == nodeR: # 단말 노드일 경우
        tree[node] = 1 # 단말 노드에 값 저장
        return tree[node]
    mid = (nodeL+nodeR)//2
    tree[node] = init(tree, node*2, nodeL, mid) + init(tree, node*2+1, mid+1, nodeR)
    return tree[node]

def update(tree, target, diff, node, nodeL, nodeR):
    if not (nodeL <= target and target <= nodeR): # 값을 변경할 노드가 구간에 있을 경우
        return
    tree[node] += diff # 내부 or 단말 노드의 값에 차이값 만큼 추가
    if nodeL != nodeR: # 단말 노드가 아닐 경우
        mid = (nodeL+nodeR)//2
        update(tree, target, diff, node*2, nodeL, mid)
        update(tree, target, diff, node*2+1, mid+1, nodeR)

def query(tree, num, node, nodeL, nodeR):
    global target
    if target: # i번째 원소가 저장될 위치(노드)를 찾았을 경우
        return
    if nodeL == nodeR: # 단말 노드일 경우
        target = nodeL # 노드 번호(i번째 원소가 저장될 위치) 저장
        return
    mid = (nodeL+nodeR)//2
    if tree[node*2] >= num: # 왼쪽 구간에 있는 원소 개수의 합이 i번째 원소 앞에 있는 수들 중 i보다 큰 수들의 개수보다 크거나 같을 경우
        query(tree, num, node*2, nodeL, mid) # 왼쪽 구간 탐색
        return
    num -= tree[node*2] # 왼쪽 구간에 있는 원소 개수의 합 만큼 i번째 원소 앞에 있는 수들 중 i보다 큰 수들의 개수에서 제거
    if tree[node*2+1] >= num: # 오른쪽 구간에 있는 원소 개수의 합이 i번째 원소 앞에 있는 수들 중 i보다 큰 수들의 개수보다 크거나 같을 경우
        query(tree, num, node*2+1, mid+1, nodeR) # 오른쪽 구간 탐색

n = int(input())
answer, tree = [0]*(n+1), [0]*(1 << (int(math.ceil(math.log2(n)))+1))
init(tree, 1, 1, n) # 세그먼트 트리 생성(단말 노드를 모두 1로 초기화 = 원소 배치)
for i in range(1, n+1):
    num, target = int(input()), 0
    query(tree, num+1, 1, 1, n) # i번째 원소가 저장될 위치(노드) 찾음
    update(tree, target, -1, 1, 1, n) # 찾은 노드의 값을 1감소시켜 0으로 설정
    answer[target] = i # 찾은 위치에 i번째 원소 저장
for i in range(1, n+1):
    print(answer[i])
'''
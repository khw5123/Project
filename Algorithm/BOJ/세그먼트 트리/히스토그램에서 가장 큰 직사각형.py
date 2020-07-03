import sys
import math
sys.setrecursionlimit(10**6)
input = sys.stdin.readline

def init(tree, arr, node, nodeL, nodeR):
    if nodeL == nodeR: # 단말 노드일 경우
        tree[node] = nodeL # 단말 노드에 노드 번호(인덱스) 저장
        return
    mid = (nodeL+nodeR)//2
    init(tree, arr, node*2, nodeL, mid)
    init(tree, arr, node*2+1, mid+1, nodeR)
    # 구간에서 높이가 가장 작은 노드 번호(인덱스) 저장
    if arr[tree[node*2]] <= arr[tree[node*2+1]]:
        tree[node] = tree[node*2]
    else:
        tree[node] = tree[node*2+1]

def query(tree, l, r, node, nodeL, nodeR):
    if r < nodeL or nodeR < l: # 구간이 겹치지 않는 경우
        return -1 # 없는 노드 번호(인덱스) 반환
    if l <= nodeL and nodeR <= r: # 구간이 완전히 포함되는 경우
        return tree[node] # 구간에서 높이가 가장 작은 노드 번호(인덱스) 반환
    mid = (nodeL+nodeR)//2
    minIdxL = query(tree, l, r, node*2, nodeL, mid) # 왼쪽 구간에서 높이가 가장 작은 노드 번호(인덱스)
    minIdxR = query(tree, l, r, node*2+1, mid+1, nodeR) # 오른쪽 구간에서 높이가 가장 작은 노드 번호(인덱스)
    if minIdxL == -1: # 왼쪽 구간이 겹치지 않는 경우
        return minIdxR
    elif minIdxR == -1: # 오른쪽 구간이 겹치지 않는 경우
        return minIdxL
    else: # 모든 구간이 완전히 포함되는 경우
        # 구간에서 높이가 가장 작은 노드 번호(인덱스) 반환
        if arr[minIdxL] <= arr[minIdxR]:
            return minIdxL
        else:
            return minIdxR

def solution(tree, arr, l, r):
    minIdx = query(tree, l, r, 1, 1, n) # 구간에서 높이가 가장 작은 노드 번호(인덱스)
    area = (r-l+1)*arr[minIdx] # 직사각형의 최대 넓이 = 너비 x 높이
    if l <= minIdx-1: # 왼쪽에 막대가 있을 경우
        areaL = solution(tree, arr, l, minIdx-1) # 왼쪽 구간 직사각형의 최대 넓이
        if area < areaL: # 왼쪽 구간 직사각형의 넓이가 더 클 경우
            area = areaL # 넓이 갱신
    if minIdx+1 <= r: # 오른쪽에 막대가 있을 경우
        areaR = solution(tree, arr, minIdx+1, r) # 오른쪽 구간 직사각형의 최대 넓이
        if area < areaR: # 오른쪽 구간 직사각형의 넓이가 더 클 경우
            area = areaR # 넓이 갱신
    return area # 직사각형의 최대 넓이 반환

MAX = 1000000000
while True:
    tmp = list(map(int, input().split()))
    if len(tmp) == 1:
        break
    n, arr = tmp[0], [0] + tmp[1:]
    tree = [0]*(1 << (int(math.ceil(math.log2(n)))+1))
    init(tree, arr, 1, 1, n) # 세그먼트 트리 생성
    print(solution(tree, arr, 1, n))
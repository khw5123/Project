import sys
sys.setrecursionlimit(10**6)

def haveCycle(node, directedGraph, visit):
    if visit[node]: # DFS를 진행한 적이 있는 노드일 경우
        if visit[node] == -1: # DFS가 진행 중인데 현재 DFS를 또 진행하고 있으므로 사이클 존재(DFS 중복)
            return True
        return False # 전에 DFS를 진행했었지만 DFS가 종료된 경우(DFS 중복 아님)
    visit[node] = -1 # 해당 노드에서 DFS 진행 중인 상태로 설정
    for _next in directedGraph[node]:
        if haveCycle(_next, directedGraph, visit): # 사이클이 존재할 경우
            return True
    visit[node] = 1 # 해당 노드 DFS 종료 상태로 설정(DFS 진행 완료 상태로 설정)
    return False # 사이클이 존재하지 않을 경우

def makeDirectedGraph(node, parent, adj, directedGraph):
    for _next in adj[node]:
        if _next != parent: # 방문하지 않은 노드일 경우
            directedGraph[_next].append(node) # 부모-자식 노드 관계가 반대인 방향 그래프 설정
            makeDirectedGraph(_next, node, adj, directedGraph)

def solution(n, path, order):
    adj, directedGraph, visit = [[] for _ in range(n)], [[] for _ in range(n)], [0]*n
    for parent, node in path:
        adj[parent].append(node) # 무방향 그래프 생성
        adj[node].append(parent)
    makeDirectedGraph(0, -1, adj, directedGraph) # 방향 그래프 생성
    for parent, node in order:
        directedGraph[node].append(parent) # 순서에 대해서도 반대 관계로 방향 그래프 설정
    for node in range(n): # 모든 노드를 시작점으로 설정
        if haveCycle(node, directedGraph, visit): # 방향 그래프에 사이클이 있을 경우
            return False # 동굴의 모든 방을 탐험할 수 없음
    return True # 방향 그래프에 사이클이 없을 경우 동굴의 모든 방을 탐험할 수 있음
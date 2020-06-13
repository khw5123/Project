import sys
input = sys.stdin.readline

def find(a):
    if a == li[a]:
        return a
    li[a] = find(li[a])
    return li[a]

def union(a, b):
    a, b = find(a), find(b)
    if a != b: # 같은 친구 네트워크가 아닐 경우
        li[a] = b # 인덱스 a를 경유지로 b를 목적지로 설정
        answer[b] += answer[a] # 두 친구 네트워크 결합. 인덱스 b를 목적지로 설정했으므로 그쪽에 결합해야 함
        answer[a] = 1 # 결합 후 경유지 네트워크 초기화
    return answer[b] # 두 친구 네트워크에 있는 사람 수 반환

for _ in range(int(input())):
    f = int(input())
    li, di = [i for i in range(200000)], {}
    answer = [1]*200000 # 친구 네트워크. 처음에는 자기 자신밖에 없으므로 1로 초기화
    num = 0
    for _ in range(f):
        a, b = map(str, input().split())
        if a not in di:
            di[a] = num
            num += 1
        if b not in di:
            di[b] = num
            num += 1
        print(union(di[a], di[b]))
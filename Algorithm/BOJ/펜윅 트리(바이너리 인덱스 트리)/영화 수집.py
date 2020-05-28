def update(tree, index, diff):
    while index < len(tree):
        tree[index] += diff
        index += (index & (-index))

def _sum(tree, index):
    result = 0
    while index > 0:
        result += tree[index]
        index -= (index & (-index))
    return result

for _ in range(int(input())):
    n, m = map(int, input().split()) # 영화 수, 보려고 하는 영화 수
    movie = list(map(int, input().split())) # 보려고 하는 영화 번호
    # 트리 크기를 (보려고 하는 영화 수 + 영화 수)로 설정
    tree, pos = [0]*(m+n+1), [0]*(n+1) # 영화의 위치
    answer = []
    # 보려고 하는 영화 수 + 1 위치부터 영화를 저장함으로써 위쪽에 본 영화가 쌓일 공간 확보(핵심 아이디어)
    for i in range(m+1, m+n+1):
        update(tree, i, 1) # 해당 위치에 영화 개수(1) 저장해서 트리 구성
        pos[i-m] = i # 영화 위치 저장
    for i in range(m):
        # 현재 영화보다 위에 있는 영화들 개수 저장. 자기 자신은 제외해야 하므로 1 차감
        answer.append(_sum(tree, pos[movie[i]]-1))
        update(tree, pos[movie[i]], -1) # 본(현재) 영화를 제일 위로 올려야 하므로 현재 영화 위치의 영화 개수 1 차감
        pos[movie[i]] = m-i # 본(현재) 영화 위치를 제일 위로 변경
        update(tree, pos[movie[i]], 1) # 제일 위에 영화 개수(1) 저장
    for v in answer:
        print(v, end=' ')
    print()
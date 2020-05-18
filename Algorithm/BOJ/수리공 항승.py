def solution(l, position):
    answer, idx = 0, 0
    position.sort()
    while idx != len(position):
        end = position[idx]+l
        for i in range(idx, len(position)):
            if position[i] >= end:
                idx = i
                break
            if i == len(position)-1:
                idx = len(position)
        answer += 1
    return answer

n, l = map(int, input().split())
position = list(map(int, input().split()))
print(solution(l, position))
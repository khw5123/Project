import sys

def solution(n, score):
    answer, idx, prev = 0, 0, -1
    score.sort()
    while idx != prev:
        prev = idx
        for i in range(idx+1, n):
            if score[idx][0] == score[i][0] or score[idx][1] >= score[i][1]:
                idx = i
                break
        answer += 1
    return answer

for i in range(int(input())):
    n, score = int(input()), []
    for i in range(n):
        score.append(list(map(int, sys.stdin.readline().split())))
    print(solution(n, score))
import math

def solution(x1, y1, r1, x2, y2, r2):
    answer = 0
    distance = math.sqrt(pow(x1-x2, 2) + pow(y1-y2, 2))
    if x1 == x2 and y1 == y2 and r1 == r2:
        answer = -1
    elif distance > abs(r1-r2) and distance < r1+r2:
        answer = 2
    elif distance == r1+r2 or distance == abs(r1-r2):
        answer = 1
    elif distance > r1+r2 or distance < abs(r1-r2):
        answer = 0
    return answer

for _ in range(int(input())):
    x1, y1, r1, x2, y2, r2 = map(int, input().split())
    print(solution(x1, y1, r1, x2, y2, r2))
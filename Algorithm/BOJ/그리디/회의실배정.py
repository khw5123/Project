import sys

def solution(n, timetable):
    answer, dp = 0, [0]*n
    timetable.sort(key=lambda x:(x[1],x[0]))
    while True:
        result, path, confirm = 0, [], True
        try:
            start = dp.index(0)
        except:
            break
        for i in range(start, len(timetable)):
            if len(path) == 0:
                path.append(i)
            else:
                if timetable[path[-1]][1] <= timetable[i][0]:
                    if dp[i] != 0:
                        count = len(path)
                        for idx in path:
                            dp[idx] = count + dp[i]
                            count -= 1
                        result = len(path) + dp[i]
                        confirm = False
                        break
                    else:
                        path.append(i)
        if confirm:
            count = len(path)
            for idx in path:
                dp[idx] = count
                count -= 1
            result = len(path)
        if answer < result:
            answer = result
        else:
            break
    return answer

n = int(input())
timetable = []
for _ in range(n):
    a, b = map(int, sys.stdin.readline().split())
    timetable.append([a, b])
print(solution(n, timetable))
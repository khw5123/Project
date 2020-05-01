import copy

def solve(path):
    global result
    if len(result) < len(path):
        result = copy.deepcopy(path)
    for i in range(len(li)):
        if li[i][path[-1][1]] == 1:
            solve(path+[[path[-1][1], i]])

for t in range(int(input())):
    n = int(input())
    save = list(map(int, input().split()))
    li = [[0]*(max(save)+1) for _ in range(max(save)+1)]
    result, answer = [], ''
    for i in range(0, len(save)-1, 2):
        li[save[i+1]][save[i]] = 1
    for i in range(0, len(save)-1, 2):
        solve([[save[i], save[i+1]]])
    for i in range(len(result)):
        answer += str(result[i][0]) + ' ' + str(result[i][1]) + ' '
    print('#' + str(t+1), answer)
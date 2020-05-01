def solve2(start):
    result = 0
    queue = [start]
    while queue:
        node = queue[0]
        del queue[0]
        result += 1
        if node in di:
            for i in range(len(di[node])):
                queue.append(di[node][i])
    return result

def solve(start):
    result = []
    queue = [start]
    while queue:
        node = queue[0]
        del queue[0]
        result.append(node)
        for k, v in di.items():
            if node in v:
                queue.append(k)
                break
    return result

for t in range(int(input())):
    v, e, a, b = map(int, input().split())
    li = list(map(int, input().split()))
    di = {}
    answer = [0, 0]
    for i in range(0, len(li)-1, 2):
        if li[i] not in di:
            di[li[i]] = [li[i+1]]
        else:
            di[li[i]].append(li[i+1])
    path_a, path_b = solve(a), solve(b)
    for i in range(len(path_a)):
        if path_a[i] in path_b:
            answer[0] = path_a[i]
            break
    answer[1] = solve2(answer[0])
    print('#' + str(t+1), answer[0], answer[1])
for t in range(int(input())):
    n, m, k = map(int, input().split())
    group = [list(map(int, input().split())) for _ in range(k)]
    for _ in range(m):
        meet = {}
        for i in range(len(group)):
            if group[i][2]:
                if group[i][3] == 1:
                    group[i][0] -= 1
                elif group[i][3] == 2:
                    group[i][0] += 1
                elif group[i][3] == 3:
                    group[i][1] -= 1
                elif group[i][3] == 4:
                    group[i][1] += 1
                if group[i][0] == 0:
                    group[i][2], group[i][3] = group[i][2]//2, 2
                elif group[i][0] == n-1:
                    group[i][2], group[i][3] = group[i][2]//2, 1
                elif group[i][1] == 0:
                    group[i][2], group[i][3] = group[i][2]//2, 4
                elif group[i][1] == n-1:
                    group[i][2], group[i][3] = group[i][2]//2, 3
                if (group[i][0], group[i][1]) not in meet:
                    meet[(group[i][0], group[i][1])] = [i, group[i][2]]
                else:
                    max_idx, max_cnt = meet[(group[i][0], group[i][1])]
                    if group[i][2] > max_cnt:
                        meet[(group[i][0], group[i][1])] = [i, group[i][2]]
                        group[i][2] += group[max_idx][2]
                        group[max_idx][2] = 0
                    else:
                        group[max_idx][2] += group[i][2]
                        group[i][2] = 0
    answer = sum(map(lambda x:x[2], group))
    print('#' + str(t+1), str(answer))

'''
import copy

for t in range(int(input())):
    n, m, k = map(int, input().split())
    group = [list(map(int, input().split())) for _ in range(k)]
    answer = 0
    for _ in range(m):
        pos, meets = [], {}
        for i in range(len(group)):
            if group[i]:
                if group[i][3] == 1:
                    group[i][0] -= 1
                elif group[i][3] == 2:
                    group[i][0] += 1
                elif group[i][3] == 3:
                    group[i][1] -= 1
                else:
                    group[i][1] += 1
                if [group[i][0], group[i][1]] in pos:
                    if (group[i][0], group[i][1]) in meets:
                        meets[(group[i][0], group[i][1])].append(i)
                    else:
                        meets[(group[i][0], group[i][1])] = []
                        meets[(group[i][0], group[i][1])].append(pos.index([group[i][0], group[i][1]]))
                        meets[(group[i][0], group[i][1])].append(i)
                pos.append([group[i][0], group[i][1]])
                if group[i][0] == 0:
                    group[i][3] = 2
                    group[i][2] //= 2
                elif group[i][0] == n-1:
                    group[i][3] = 1
                    group[i][2] //= 2
                elif group[i][1] == 0:
                    group[i][3] = 4
                    group[i][2] //= 2
                elif group[i][1] == n-1:
                    group[i][3] = 3
                    group[i][2] //= 2
                if group[i][2] == 0:
                    group[i] = []
            else:
                pos.append([])
        if meets:
            for _, meet in meets.items():
                max_count, max_idx, sum_ = 0, 0, 0
                for i in range(len(meet)):
                    sum_ += group[meet[i]][2]
                    if group[meet[i]][2] > max_count:
                        max_count = group[meet[i]][2]
                        max_idx =  meet[i]
                tmp = copy.deepcopy(group[max_idx])
                tmp[2] = sum_
                for idx in meet:
                    group[idx] = []
                group[meet[0]] = tmp
    for i in range(len(group)):
        if group[i]:
            answer += group[i][2]
    print('#' + str(t+1), str(answer))
'''
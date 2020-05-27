import copy

def solution(n, k, goods):
    answer = 0
    multitap = set()
    for i in range(len(goods)):
        if len(multitap) == n:
            if goods[i] not in multitap:
                tmp = copy.deepcopy(list(multitap))
                for j in range(i+1, len(goods)):
                    if len(tmp) == 1:
                        break
                    if goods[j] in tmp:
                        tmp.remove(goods[j])
                multitap.remove(tmp[0])
                multitap.add(goods[i])
                answer += 1
        else:
            multitap.add(goods[i])
    return answer

n, k = map(int, input().split())
goods = list(map(int, input().split()))
print(solution(n, k, goods))
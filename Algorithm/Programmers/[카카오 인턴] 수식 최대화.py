import copy
from itertools import permutations

def solution(expressions):
    answer = 0
    li, save, num = [], [], ''
    for exp in expressions:
        if exp in '+-*':
            li.append(num)
            num = ''
            li.append(exp)
            if exp not in save:
                save.append(exp)
        else:
            num += exp
    li.append(num)
    def solve(lis, exp):
        result, idx = 0, 0
        while len(lis) != 1:
            confirm = True
            for i in range(len(lis)):
                if lis[i] == exp[idx]:
                    if lis[i] == '+':
                        n = int(lis[i-1]) + int(lis[i+1])
                        for _ in range(3):
                            del lis[i-1]
                        lis.insert(i-1, n)
                    elif lis[i] == '-':
                        n = int(lis[i-1]) - int(lis[i+1])
                        for _ in range(3):
                            del lis[i-1]
                        lis.insert(i-1, n)
                    elif lis[i] == '*':
                        n = int(lis[i-1]) * int(lis[i+1])
                        for _ in range(3):
                            del lis[i-1]
                        lis.insert(i-1, n)
                    confirm = False
                    break
            if confirm:
                idx += 1
        result = abs(lis[0])
        return result
    for exp in list(permutations(save, len(save))):
        answer = max(answer, solve(copy.deepcopy(li), exp))
    return answer
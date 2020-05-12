import copy

def solution(k, A):
    answer = ''
    max_ = copy.deepcopy(A)
    for i in range(0, 2*len(max_)+1, 2):
        max_.insert(i, '')
    num = 9
    for i in range(len(max_)):
        if max_[i] == '>':
            for j in range(i-1, -1, -2):
                if max_[j] == '':
                    max_[j] = str(num)
                    num -= 1
                else:
                    break
    for i in range(len(max_)-1, -1, -1):
        if max_[i] == '':
            max_[i] = str(num)
            num -= 1
    for i in range(0, len(max_), 2):
        answer += max_[i]
    return answer

def solution2(k, A):
    answer = ''
    min_ = copy.deepcopy(A)
    for i in range(0, 2*len(min_)+1, 2):
        min_.insert(i, '')
    num = len(min_)//2
    for i in range(len(min_)-1, -1, -1):
        if min_[i] == '<':
            for j in range(i+1, len(min_), 2):
                if min_[j] == '':
                    min_[j] = str(num)
                    num -= 1
                else:
                    break
    idx = set()
    for i in range(0, len(min_), 2):
        if min_[i] == '':
            if i != len(min_)-1:
                if min_[i+1] == '>':
                    idx.add(i)
        else:
            if idx:
                for index in list(set(idx)):
                    min_[index] = str(num)
                    num -= 1
            idx = set()
    if idx:
        for index in list(set(idx)):
            min_[index] = str(num)
            num -= 1
    for i in range(len(min_)-1, -1, -1):
        if min_[i] == '':
            min_[i] = str(num)
            num -= 1
    for i in range(0, len(min_), 2):
        answer += min_[i]
    return answer

k = int(input())
A = list(map(str, input().split()))
print(solution(k, A))
print(solution2(k, A))
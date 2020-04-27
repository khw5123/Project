def solution(cookie):
    answer = 0
    sum_ = [0]*len(cookie)
    sum_[0] = cookie[0]
    for i in range(len(cookie)-1):
        sum_[i+1] += sum_[i]+cookie[i+1]
    for i in range(len(cookie)):
        for j in range(i+1, len(cookie)):
            back = sum_[j]-sum_[i]
            if back > sum_[i]:
                break
            if back <= answer:
                continue
            for k in range(i+1):
                front = sum_[i]-sum_[k] if k != i else sum_[i]
                if back == front:
                    answer = max(answer, front)
                    break
    return answer

'''
import copy

def solution(cookie):
    answer = 0
    if len(cookie) != 1:
        front, back = [0]*len(cookie), copy.deepcopy(cookie)
        for i in range(len(cookie)-1):
            if i > 0:
                back[i] += back[i-1]
            if cookie[i] == cookie[i+1]:
                answer = max(answer, cookie[i])
        back[-1] += back[-2]
        for i in range(len(cookie)):
            for j in range(i+1):
                front[j] += cookie[i]
            for j in range(i+1, len(cookie)):
                back[j] -= cookie[i]
            if front[0] <= answer:
                continue
            for j in range(i+1):
                if front[j] <= answer:
                    break
                if front[j] in back[i+1:]:
                    answer = max(answer, front[j])
                    break
    return answer
'''
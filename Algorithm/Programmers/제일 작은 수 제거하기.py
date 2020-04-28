def solution(arr):
    answer = []
    if len(arr) == 1:
        answer.append(-1)
    else:
        del arr[arr.index(min(arr))]
        answer = arr
    return answer
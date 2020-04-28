def solution(arr1, arr2):
    answer = list()
    for i in range(len(arr1)):
        answer.append([])
        for k in range(len(arr2[0])):
            tmp = 0
            for j in range(len(arr1[0])):
                tmp += arr1[i][j] * arr2[j][k]
            answer[-1].append(tmp)
    return answer
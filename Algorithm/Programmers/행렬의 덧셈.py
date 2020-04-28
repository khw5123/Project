def solution(arr1, arr2):
    answer = [[]]
    for i in range(len(arr1)):
        for j in range(len(arr1[0])):
            answer[-1].append(arr1[i][j] + arr2[i][j])
        answer.append([])
    return answer[:len(answer)-1]
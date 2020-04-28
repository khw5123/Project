def solution(heights):
    answer = []
    for i in range(len(heights)-1, -1, -1):
        confirm = False
        for j in range(i-1, -1, -1):
            if heights[j] > heights[i]:
                answer.insert(0, j+1)
                confirm = True
                break
        if confirm == False:
            answer.insert(0, 0)
    return answer
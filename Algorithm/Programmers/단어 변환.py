def solve(begin, target, words, depth, answer):
    if begin[-1] == target:
        answer[0] = min(answer[0], depth)
        return depth
    tmp = list()
    for i in range(len(words)):
        diff = 0
        for j in range(len(words[i])):
            if words[i][j] != begin[-1][j]:
                diff += 1
            if diff > 1:
                break
        if diff == 1:
            if words[i] not in begin:
                tmp.append(words[i])
    for i in range(len(tmp)):
        begin.append(tmp[i])
        solve(begin, target, words, depth+1, answer)
        begin.pop()
    return depth

def solution(begin, target, words):
    answer = [len(words)]
    if target not in words:
        return 0
    else:
        solve([begin], target, words, 0, answer)
    return answer[0]
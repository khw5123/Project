def solution(progresses, speeds):
    answer = []
    save = [0 for _ in range(len(progresses))]
    while True:
        for i in range(len(progresses)):
            if progresses[i] < 100:
                progresses[i] += speeds[i]
                save[i] += 1
        confirm = True
        for i in range(len(progresses)):
            if progresses[i] < 100:
                confirm = False
                break
        if confirm:
            break
    tmp = [0 for _ in range(len(progresses))]
    for i in range(len(save)):
        tmp[i] = max(save[:i+1])
    while len(tmp) != 0:
        answer.append(tmp.count(tmp[0]))
        x = tmp[0]
        while x in tmp: tmp.remove(x)
    return answer
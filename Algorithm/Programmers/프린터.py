def solution(priorities, location):
    answer = 0
    save = list()
    for i in range(len(priorities)):
        if i == location:
            save.append([priorities[i], 1])
        else:
            save.append([priorities[i], 0])
    while True:
        answer += 1
        idx = priorities.index(max(priorities))
        if save[idx][1] == 1:
            break
        else:
            if idx != len(priorities):
                priorities = priorities[idx+1:] + priorities[:idx]
                save = save[idx+1:] + save[:idx]
            else:
                priorities = priorities[:idx]
                save = save[:idx]
    return answer
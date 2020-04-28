def solve(idx, case, save, answer):
    if idx == len(save):
        answer[tuple(sorted(case))] = 1
        return
    for i in range(len(save[idx])):
        if save[idx][i] not in case:
            case.append(save[idx][i])
            solve(idx+1, case, save, answer)
            case.pop()

def solution(user_id, banned_id):
    answer = dict()
    save = []
    for i in range(len(banned_id)):
        save.append([])
        for j in range(len(user_id)):
            if len(user_id[j]) == len(banned_id[i]):
                confirm = 0
                for k in range(len(user_id[j])):
                    if banned_id[i][k] == '*' or user_id[j][k] == banned_id[i][k]:
                        confirm += 1
                    else:
                        break
                if confirm == len(user_id[j]):
                    save[-1].append(user_id[j])
    solve(0, [], save, answer)
    return len(answer)
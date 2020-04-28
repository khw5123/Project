def solution(skill, skill_trees):
    answer = 0
    for sk in skill_trees:
        idx = 0
        for c in sk:
            if skill[idx] == c:
                idx += 1
            if idx == len(skill):
                break
            if c in skill[idx:]:
                idx = -1
        if idx != -1:
            answer += 1
    return answer
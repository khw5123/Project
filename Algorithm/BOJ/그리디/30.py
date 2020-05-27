def solution(n):
    answer = -1
    if '0' in n and sum(list(map(int, n)))%3 == 0:
        answer = int(''.join(sorted(list(map(str, n)), reverse=True)))
    return answer

n = input()
print(solution(n))
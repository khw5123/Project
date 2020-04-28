import copy

def solve(visit, tickets, route, answer):
    if len(route) == len(tickets) + 1:
        answer.append(copy.deepcopy(route))
    else:
        for i in range(len(tickets)):
            if route[-1] == tickets[i][0] and i not in visit:
                route.append(tickets[i][1])
                visit.append(i)
                solve(visit, tickets, route, answer)
                route.pop()
                visit.pop()

def solution(tickets):
    answer = []
    for i in range(len(tickets)):
        if tickets[i][0] == 'ICN':
            route = []
            route.append(tickets[i][0])
            route.append(tickets[i][1])
            solve([i], tickets, route, answer)
    answer.sort()
    return answer[0]
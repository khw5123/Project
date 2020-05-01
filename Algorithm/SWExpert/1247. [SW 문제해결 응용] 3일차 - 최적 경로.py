def solve(path, distance):
    if len(path) == len(customer):
        answer[0] = min(answer[0], distance + abs(home[0]-path[-1][0]) + abs(home[1]-path[-1][1]))
        return
    if distance >= answer[0]:
        return
    for i in range(len(customer)):
        if customer[i] not in path:
            solve(path+[customer[i]], distance + abs(path[-1][0]-customer[i][0]) + abs(path[-1][1]-customer[i][1]))

for t in range(int(input())):
    n = int(input())
    li = list(map(int, input().split()))
    home, company, customer = [li[0], li[1]], [li[2], li[3]], []
    answer = [987654321]
    for i in range(4, len(li)-1, 2):
        customer.append([li[i], li[i+1]])
    for i in range(len(customer)):
        solve([[customer[i][0], customer[i][1]]], abs(company[0]-customer[i][0]) + abs(company[1]-customer[i][1]))
    print('#' + str(t+1), answer[0])
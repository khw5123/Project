def solution(bridge_length, weight, truck_weights):
    answer = 0
    save = list()
    while True:
        remove = list()
        for i in range(len(save)):
            save[i][1] += 1
            if save[i][1] > bridge_length:
                remove.append(save[i])
        for i in range(len(remove)):
            save.remove(remove[i])
        sum_ = 0
        for i in range(len(save)):
            sum_ += save[i][0]
        if len(truck_weights) != 0 and sum_ + truck_weights[0] <= weight:
            save.append([truck_weights[0], 1])
            del truck_weights[0]
        answer += 1
        if len(truck_weights) == 0 and len(save) == 0:
            break
        # print(answer, save, truck_weights)
    return answer
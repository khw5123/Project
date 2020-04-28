def merge_sort(arr):
    if len(arr) < 2:
        return arr
    mid = len(arr) // 2
    low_arr = merge_sort(arr[:mid])
    high_arr = merge_sort(arr[mid:])
    merged_arr = []
    l = h = 0
    while l < len(low_arr) and h < len(high_arr):
        if int(low_arr[l] + high_arr[h]) < int(high_arr[h] + low_arr[l]):
            merged_arr.append(high_arr[h])
            h += 1
        else:
            merged_arr.append(low_arr[l])
            l += 1
    merged_arr += low_arr[l:]
    merged_arr += high_arr[h:]
    return merged_arr

def solution(numbers):
    answer = ''
    save = [str(n) for n in numbers]
    while True:
        tmp = save
        save = merge_sort(save)
        if tmp == save:
            break
    answer = ''.join(save)
    if int(answer) == 0:
        answer = '0'
    return answer
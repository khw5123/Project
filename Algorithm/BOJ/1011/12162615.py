count = int(input(''))
for _ in range(count):
    start, end = map(int, input().split())
    num = 1
    result = 0
    save = 0
    if end - start == 1:
        print(1)
        continue
    elif end - start == 2:
        print(2)
        continue
    while True:
        start += num
        end -= num
        # print(start, end, end='')
        result += 2
        # print('  ', num, save, result)
        if end - start == num - 1 or end - start == num or end - start == num + 1:
            print(result + 1)
            break
        elif end - start >= num * 2 - 2 and end - start <= num * 2 + 2:
            print(result + 2)
            break
        elif end - start < num or start > end:
            start -= num
            end += num
            result -= 2
            if save - num == -1 or save - num == 0:
                num -= 1
            elif save - num == 1:
                start -= save
                end += save
                num = save - 1
                save -= 1
                result -= 2
            continue
        save = num
        num += 1
def solution(brown, red):
    answer = []
    height = 3
    while True:
        width = (brown + red) / height
        if width != int(width):
            height += 1
            continue
        else:
            b, r = brown, red
            for h in range(height):
                if h == 0 or h == height-1:
                    b -= int(width)
                else:
                    b -= 2
                    r -= int(width)-2
            if b == 0 and r == 0:
                answer.append(int(width))
                answer.append(height)
                break
        if width < height:
            break
        height += 1
    return answer
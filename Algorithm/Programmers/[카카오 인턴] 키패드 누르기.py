def solution(numbers, hand):
    answer = ''
    li = [['1','2','3'], ['4','5','6'], ['7','8','9'], ['*', '0', '#']]
    left_x, left_y, right_x, right_y = 0, 3, 2, 3
    def check(n):
        nonlocal li
        x, y = -1, -1
        for i in range(4):
            for j in range(3):
                if li[i][j] == n:
                    x, y = j, i
        return x, y
    while numbers:
        n = str(numbers[0])
        del numbers[0]
        if n == '1' or n == '4' or n =='7':
            answer += 'L'
            left_x, left_y = check(n)
        elif n == '3' or n == '6' or n == '9':
            answer += 'R'
            right_x, right_y = check(n)
        else:
            target_x, target_y = check(n)
            if abs(left_x-target_x) + abs(left_y-target_y) < abs(right_x-target_x) + abs(right_y-target_y):
                answer += 'L'
                left_x, left_y = check(n)
            elif abs(left_x-target_x) + abs(left_y-target_y) > abs(right_x-target_x) + abs(right_y-target_y):
                answer += 'R'
                right_x, right_y = check(n)
            else:
                if hand == 'left':
                    answer += 'L'
                    left_x, left_y = check(n)
                else:
                    answer += 'R'
                    right_x, right_y = check(n)
    return answer
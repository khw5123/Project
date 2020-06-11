def solution(s, depth):
    if len(s) == l:
        a, b = 0, 0
        for char in s:
            if char in 'aeiou':
                a += 1
            else:
                b += 1
        if a > 0 and b > 1:
            print(s)
        return
    if depth == c:
        return
    solution(s+code[depth], depth+1)
    solution(s, depth+1)

l, c = map(int, input().split())
code = sorted(list(map(str, input().split())))
solution('', 0)
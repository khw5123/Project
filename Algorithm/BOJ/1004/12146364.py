count = int(input(''))
for _ in range(count):
    startX, startY, endX, endY = map(int, input().split())
    num = int(input(''))
    planet = []
    result = 0
    for i in range(num):
        cx, cy, r = map(int, input().split())
        planet.append([cx, cy, r])
    for i in range(num):
        if (pow(planet[i][0] - startX, 2) + pow(planet[i][1] - startY, 2) <= pow(planet[i][2], 2)) and \
            (pow(planet[i][0] - endX, 2) + pow(planet[i][1] - endY, 2) <= pow(planet[i][2], 2)):
                continue
        if pow(planet[i][0] - startX, 2) + pow(planet[i][1] - startY, 2) <= pow(planet[i][2], 2):
            result += 1
        if pow(planet[i][0] - endX, 2) + pow(planet[i][1] - endY, 2) <= pow(planet[i][2], 2):
            result += 1
    print(result)
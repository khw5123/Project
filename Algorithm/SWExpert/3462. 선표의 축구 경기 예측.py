from math import factorial

for t in range(int(input())):
    a, b = map(int, input().split())
    a, b = a/100, b/100
    probability_a, probability_b = 0., 0.
    for point in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        probability_a += ((factorial(30)/(factorial(point)*factorial(30-point))) * (pow(a, point)*(pow(1-a, 30-point))))
        probability_b += ((factorial(30)/(factorial(point)*factorial(30-point))) * (pow(b, point)*(pow(1-b, 30-point))))
    answer = 1 - ((1-probability_a) * (1-probability_b))
    print('#' + str(t+1), '%.5f' % round(answer, 5))
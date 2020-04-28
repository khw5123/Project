def solution(str1, str2):
    answer = 0
    s1, s2 = list(), list()
    for i in range(len(str1)-1):
        if str1[i].isalpha() and str1[i+1].isalpha():
            s1.append(str1[i:i+2].lower())
    for i in range(len(str2)-1):
        if str2[i].isalpha() and str2[i+1].isalpha():
            s2.append(str2[i:i+2].lower())
    intersection, union = 0, 0
    while True:
        duplicate = False
        for i in range(len(s1)):
            for j in range(len(s2)):
                if s1[i] == s2[j]:
                    intersection += 1
                    duplicate = True
                    del s1[i]
                    del s2[j]
                    break
            if duplicate:
                break
        if duplicate == False:
            union = intersection + len(s1) + len(s2)
            break
    if intersection == 0 and union == 0:
        intersection, union = 1, 1
    answer = int((intersection / union) * 65536)
    return answer
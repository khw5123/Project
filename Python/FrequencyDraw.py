# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import random

def main():
    frequency = []
    time = []
    count = 100 # 테스트용
    time_tmp = 0
    period = 1.0
    plt.ion()
    plt.ylim(0, 200)
    plt.xlabel('time')
    plt.ylabel('frequency')
    while True:
        count += 10*random.randrange(-1,2) # 테스트용
        frequency.append(count)
        time_tmp += period
        time.append(time_tmp)
        plt.plot(time, frequency)
        plt.grid()
        plt.show()
        print count
        plt.pause(period)
        plt.grid()
        
if __name__ == '__main__':
    main()

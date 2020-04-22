# -*- coding: utf-8 -*-
import numpy as np
import pylab
from scipy.io.wavfile import write
import os
# http://picosanta.tistory.com/13

# sampling rate
Fs = 44100.0 # Hz

# play length
tlen = float(raw_input('Input Play Time(s): ')) # 소리 지속 시간
Ts = 1/Fs # sampling interval
t = np.arange(0, tlen, Ts) # time array

# generate signal
sin_freq = float(raw_input('Input Frequency : ')) # 주파수
signal = np.sin(2*np.pi*sin_freq*t)

# generate noise
noise = 0 # np.random.uniform(-1, 1, len(t))*0.1

# signal + noise
signal_n = signal + noise
 
# fft
signal_f = np.fft.fft(signal_n)
freq = np.fft.fftfreq(len(t), Ts)

# plot
pylab.plot(freq, 20*np.log10(np.abs(signal_f)))
pylab.xlim(0, Fs/2)
pylab.show()

# save as wav file
scaled = np.int16(signal_n/np.max(np.abs(signal_n)) * 32767)
write('test.wav', Fs, scaled)

# play wav file
os.system("test.wav")

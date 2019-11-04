# -*- coding: utf-8 -*-
import numpy as np
import wave
import struct

def main():
    fname = raw_input('Input wav file name(.wav): ')
    data_size = 40000 
    frate = 44100.0
    wav_file = wave.open(fname, 'r')
    data = wav_file.readframes(data_size)
    wav_file.close()
    data = struct.unpack('{n}h'.format(n=data_size), data)
    data = np.array(data)
    w = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(w))
    # print(freqs.min(), freqs.max())
    idx = np.argmax(np.abs(w))
    freq = freqs[idx]
    freq_in_hertz = abs(freq * frate)
    print 'Frequency : ', int(round(freq_in_hertz))

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
import pyaudio
import wave

def play(fname):
	CHUNK = 1024

	wf = wave.open(fname, 'rb')

	p = pyaudio.PyAudio()

	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
					channels=wf.getnchannels(),
					rate=wf.getframerate(),
					output=True)

	data = wf.readframes(CHUNK)

	while data != '':
		stream.write(data)
		data = wf.readframes(CHUNK)

	stream.stop_stream()
	stream.close()

	p.terminate()

def main():
	fname = raw_input('Input Wav File(.wav): ')
	play(fname)

if __name__ == '__main__':
	main()
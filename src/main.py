#!/usr/bin/python3

import pyaudio
import wave
import audioop
import signal
from servo import Servo
from audio_threshold import AudioThreshold

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"


def sig_handler(signum, frame):
    stream.stop_stream()
    stream.close()
    p.terminate()
    exit(1)


signal.signal(signal.SIGINT, sig_handler)

s = Servo()
at = AudioThreshold()
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


while True:
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)
    at.add(rms)

    if (at.above_threshold()):
        s.zap()

    print(rms)


stream.stop_stream()
stream.close()
p.terminate()

# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()

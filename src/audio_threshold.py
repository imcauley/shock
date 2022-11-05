import collections


class AudioThreshold:
    def __init__(self):
        self.rms_buffer = collections.deque(maxlen=40)
        self.THRESHOLD = 100

    def add(self, value):
        self.rms_buffer.append(value)

    def above_threshold(self):
        return self.mean() < self.THRESHOLD

    def mean(self):
        l = list(self.rms_buffer)
        return sum(l) / len(l)

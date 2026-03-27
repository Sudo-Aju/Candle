import pyaudio
import numpy as np
from collections import deque

class AudioProcessor:
    def __init__(self, config):
        self.config = config
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100,
                                  input=True, frames_per_buffer=1024)
        self.threshold = self.config.settings["MIC_THRESHOLD"]
        self.history = deque(maxlen=10)

    def get_blow_intensity(self) -> float:
        try:
            raw_data = self.stream.read(1024, exception_on_overflow=False)
            data = np.frombuffer(raw_data, dtype=np.int16).astype(np.float64)
            rms = float(np.sqrt(np.mean(data**2)))
            
            self.history.append(rms)
            avg_rms = sum(self.history) / len(self.history)
            
            intensity = max(0.0, (avg_rms - self.threshold) / 4000.0)
            return min(intensity, 3.0)
        except Exception:
            return 0.0

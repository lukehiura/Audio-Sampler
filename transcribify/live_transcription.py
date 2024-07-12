# live_transcription

import pyaudio
import wave
import threading
import numpy as np

class LiveTranscriber:
    def __init__(self, init_transcription_func):
        self.transcribe = init_transcription_func()
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.transcription = ""

    def start_recording(self):
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000,
                                      input=True,
                                      frames_per_buffer=1024)
        self.is_recording = True
        self.frames = []
        
        def record():
            while self.is_recording:
                try:
                    data = self.stream.read(1024, exception_on_overflow=False)
                    self.frames.append(data)
                    if len(self.frames) % 16 == 0:  # Process every ~1 second of audio
                        self.transcribe_chunk()
                except IOError as e:
                    if e.errno == pyaudio.paInputOverflowed:
                        print("Input overflowed. Some audio data was lost.")
                    else:
                        raise
        
        threading.Thread(target=record, daemon=True).start()

    def stop_recording(self):
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.transcribe_chunk()  # Transcribe any remaining audio

    def transcribe_chunk(self):
        if not self.frames:
            return
        
        audio_data = b''.join(self.frames[-16:])  # Last ~1 second of audio
        audio_array = np.frombuffer(audio_data, dtype=np.int16).flatten().astype(np.float32) / 32768.0
        
        transcription = self.transcribe(audio_array)
        self.transcription += " " + transcription
        return transcription

    def save_audio(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def get_transcription(self):
        return self.transcription.strip()

    def clear_transcription(self):
        self.transcription = ""
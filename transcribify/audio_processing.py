from pydub import AudioSegment
import os
import tempfile

def convert_audio(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.m4a':
        audio = AudioSegment.from_file(file_path, format="m4a")
    else:
        audio = AudioSegment.from_file(file_path)

    audio = audio.set_frame_rate(16000).set_channels(1)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp_file.name, format="wav")
    return temp_file.name
import os
from .models import transcription_pipeline, diarization_pipeline
from .audio_processing import convert_audio

def transcribe_audio(file_path):
    if transcription_pipeline is None:
        raise Exception("Transcription model not initialized properly.")
    
    audio_file = convert_audio(file_path)
    result = transcription_pipeline(audio_file, return_timestamps=True)
    os.remove(audio_file)
    return result["text"]

def diarize_audio(file_path):
    if diarization_pipeline is None:
        raise Exception("Diarization model not initialized properly.")
    
    audio_file = convert_audio(file_path)
    diarization = diarization_pipeline(audio_file)
    os.remove(audio_file)
    return diarization
import logging
import os
from .models import initialize_models
from .audio_processing import convert_audio

logger = logging.getLogger(__name__)

def transcribe_audio(file_path, init_transcription):
    transcribe = init_transcription()
    if transcribe is None:
        logger.error("Transcription model not initialized properly.")
        return "Transcription is not available."
    
    audio_file = convert_audio(file_path)
    result = transcribe(audio_file)
    os.remove(audio_file)
    return result

def diarize_audio(file_path, init_diarization):
    diarization_pipeline = init_diarization()
    if diarization_pipeline is None:
        logger.error("Diarization model not initialized properly.")
        return None
    
    audio_file = convert_audio(file_path)
    diarization = diarization_pipeline(audio_file)
    os.remove(audio_file)
    return diarization
# models.py

import logging
from pyannote.audio import Pipeline
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def initialize_models():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Get the Hugging Face access token
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token:
        logger.error("HUGGINGFACE_TOKEN not found in environment variables.")
        return None, None

    # Initialize transcription pipeline (lazy loading)
    def init_transcription():
        try:
            processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
            model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")
            model.to(device)

            def transcribe(audio):
                input_features = processor(audio, sampling_rate=16000, return_tensors="pt").input_features
                input_features = input_features.to(device)
                
                with torch.no_grad():
                    predicted_ids = model.generate(input_features)
                
                transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
                return transcription[0]

            logger.info("Transcription model initialized successfully.")
            return transcribe
        except Exception as e:
            logger.error(f"Error initializing transcription model: {str(e)}")
            return None

    # Initialize diarization pipeline (lazy loading)
    def init_diarization():
        try:
            diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                                            use_auth_token=hf_token)
            logger.info("Diarization model initialized successfully.")
            return diarization_pipeline
        except Exception as e:
            logger.error(f"Error initializing diarization model: {str(e)}")
            return None

    return init_transcription, init_diarization

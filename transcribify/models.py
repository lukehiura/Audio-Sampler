import torch
import time
from transformers import pipeline, AutoProcessor, AutoModelForSpeechSeq2Seq
from pyannote.audio import Pipeline
from huggingface_hub import login
import subprocess

transcription_pipeline = None
diarization_pipeline = None

def hf_login():
    try:
        subprocess.run(["huggingface-cli", "login"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Failed to login using CLI. Please try manual login.")
        return False

def initialize_models():
    global transcription_pipeline, diarization_pipeline
    
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        processor = AutoProcessor.from_pretrained("openai/whisper-large-v3")
        model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large-v3")
        model.to(device)

        transcription_pipeline = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            device=device,
            generate_kwargs={"language": "en"}
        )
    except Exception as e:
        print(f"Error initializing transcription model: {str(e)}")
        transcription_pipeline = None

    try:
        diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                                        use_auth_token=True)
        print("Diarization model initialized successfully.")
    except Exception as e:
        print(f"Error initializing primary diarization model: {str(e)}")
        print("Attempting to use alternative model...")
        try:
            # Try an alternative model
            diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                                            use_auth_token=True)
            print("Alternative diarization model initialized successfully.")
        except Exception as e:
            print(f"Error initializing alternative diarization model: {str(e)}")
            print("Diarization will not be available.")
            diarization_pipeline = None

    return transcription_pipeline, diarization_pipeline
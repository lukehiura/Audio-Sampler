import warnings
from transformers import logging

# Suppress the Torchaudio warning
warnings.filterwarnings("ignore", message="Torchaudio's I/O functions now support par-call bakcend dispatch")

# Suppress the Transformers special tokens message
logging.set_verbosity_error()

# Your existing imports and code here
from transcribify import initialize_models, create_gui

if __name__ == "__main__":
    initialize_models()
    create_gui()
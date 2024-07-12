# Audio Transcriber

Audio Transcriber is a Python tool for transcribing audio files with optional speaker diarization. It provides both a GUI and a programmable interface for easy audio transcription.

## Features

- Transcribe audio files to text
- Optional speaker diarization
- User-friendly GUI
- Export results to HTML

## Installation

### Prerequisites

- Python 3.7 or higher

### Setup

We use `uv` for managing virtual environments and package installation. Follow these steps to set up the project:

#### On macOS and Linux:

```sh
# Download the setup script
curl -O https://raw.githubusercontent.com/yourusername/audio_transcriber/main/setup.sh

# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

#### On Windows:

```powershell
# Download the setup script
Invoke-WebRequest -Uri https://raw.githubusercontent.com/yourusername/audio_transcriber/main/setup.ps1 -OutFile setup.ps1

# Set execution policy to run the script
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Run the setup script
.\setup.ps1
```

These scripts will:
1. Install `uv` if it's not already installed
2. Create a virtual environment
3. Activate the virtual environment
4. Install all required packages

## Usage

### GUI

To run the GUI:

```sh
python examples/simple_gui.py
```

### Programmatic Usage

```python
from audio_transcriber import initialize_models, transcribe_audio, diarize_audio

# Initialize models
initialize_models()

# Transcribe audio
transcription = transcribe_audio("path/to/your/audio/file.mp3")
print(transcription)

# Diarize audio (if available)
diarization = diarize_audio("path/to/your/audio/file.mp3")
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"Speaker {speaker}: {turn.start:.2f} - {turn.end:.2f}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Notes

While FFmpeg is not a direct requirement for this project, some underlying libraries may use it for certain audio processing tasks. If you encounter any issues with audio file handling, consider installing FFmpeg as an additional step.
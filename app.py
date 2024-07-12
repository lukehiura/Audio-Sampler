import streamlit as st
import os
import tempfile
from transcribify import initialize_models, transcribe_audio, diarize_audio, LiveTranscriber

# Initialize models
init_transcription, init_diarization = initialize_models()
live_transcriber = LiveTranscriber(init_transcription)

def main():
    st.title('Transcribify Demo')

    # File upload
    uploaded_file = st.file_uploader("Choose an audio file", type=['mp3', 'wav', 'ogg', 'flac', 'm4a'])

    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        # Transcribe
        if st.button('Transcribe'):
            with st.spinner('Transcribing... Please wait.'):
                transcription = transcribe_audio(tmp_file_path, init_transcription)
                st.text_area("Transcription", transcription, height=200)

        # Diarize
        if st.button('Diarize'):
            with st.spinner('Performing speaker diarization... Please wait.'):
                diarization = diarize_audio(tmp_file_path, init_diarization)
                diarization_text = "Diarization:\n"
                for turn, _, speaker in diarization.itertracks(yield_label=True):
                    diarization_text += f"Speaker {speaker}: {turn.start:.2f} - {turn.end:.2f}\n"
                st.text_area("Diarization", diarization_text, height=200)

        # Clean up temporary file
        os.unlink(tmp_file_path)

    # Live transcription
    if st.button('Start Live Transcription'):
        live_transcriber.start_recording()
        st.text_area("Live Transcription", live_transcriber.get_transcription(), height=200)
        if st.button('Stop'):
            live_transcriber.stop_recording()

if __name__ == "__main__":
    main()
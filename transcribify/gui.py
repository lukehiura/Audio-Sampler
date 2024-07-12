import PySimpleGUI as sg
import threading
from .transcription import transcribe_audio, diarize_audio
from .utils import save_to_html
from .models import initialize_models
from .live_transcription import LiveTranscriber

def create_gui():
    sg.theme('LightBlue2')

    file_column = [
        [sg.Text('Audio File:'), sg.Input(key='-FILE-'), sg.FileBrowse(file_types=(("Audio Files", "*.mp3 *.wav *.ogg *.flac *.m4a"),))],
        [sg.Checkbox('Perform Speaker Diarization (if available)', key='-DIARIZE-')],
        [sg.Text('Output HTML File:'), sg.Input(key='-OUTPUT-', default_text='transcription.html')],
        [sg.Button('Transcribe File'), sg.Button('Exit')]
    ]

    live_column = [
        [sg.Button('Start Recording', key='-RECORD-'), sg.Button('Stop Recording', key='-STOP-', disabled=True)],
        [sg.Button('Save Transcription', key='-SAVE-', disabled=True)],
        [sg.Text('Live Transcription:')],
        [sg.Multiline(size=(60, 10), key='-LIVE-OUTPUT-', autoscroll=True, disabled=True)]
    ]

    layout = [
        [sg.Text('Audio Transcription Tool', font=('Helvetica', 16))],
        [sg.Column(file_column), sg.VSeperator(), sg.Column(live_column)],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS-')],
        [sg.Multiline(size=(120, 15), key='-OUTPUT-', autoscroll=True)]
    ]

    window = sg.Window('Enhanced Audio Transcription', layout, finalize=True)

    # Initialize models and live transcriber
    initialize_models()
    live_transcriber = LiveTranscriber()

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        
        if event == 'Transcribe File':
            file_path = values['-FILE-']
            if not file_path:
                sg.popup_error("Please select an audio file.")
                continue
            
            window['-OUTPUT-'].update("Transcribing... Please wait.\n")
            window['-PROGRESS-'].update(0)
            
            def transcribe_thread():
                try:
                    transcription = transcribe_audio(file_path)
                    window.write_event_value('-TRANSCRIPTION-DONE-', transcription)
                    
                    if values['-DIARIZE-']:
                        window.write_event_value('-DIARIZATION-START-', None)
                        diarization = diarize_audio(file_path)
                        window.write_event_value('-DIARIZATION-DONE-', diarization)
                    else:
                        window.write_event_value('-PROCESS-COMPLETE-', None)
                except Exception as e:
                    window.write_event_value('-ERROR-', str(e))

            threading.Thread(target=transcribe_thread, daemon=True).start()

        elif event == '-RECORD-':
            window['-RECORD-'].update(disabled=True)
            window['-STOP-'].update(disabled=False)
            window['-LIVE-OUTPUT-'].update('')
            live_transcriber.clear_transcription()
            live_transcriber.start_recording()

        elif event == '-STOP-':
            window['-RECORD-'].update(disabled=False)
            window['-STOP-'].update(disabled=True)
            window['-SAVE-'].update(disabled=False)
            live_transcriber.stop_recording()
            window['-LIVE-OUTPUT-'].update(live_transcriber.get_transcription())

        elif event == '-SAVE-':
            save_path = sg.popup_get_file('Save Transcription', save_as=True, file_types=(("Text Files", "*.txt"),))
            if save_path:
                with open(save_path, 'w') as f:
                    f.write(live_transcriber.get_transcription())
                sg.popup(f"Transcription saved to {save_path}")

        elif event == '-TRANSCRIPTION-DONE-':
            transcription = values[event]
            window['-OUTPUT-'].update(f"Transcription:\n{transcription}\n\n")
            window['-PROGRESS-'].update(50)

        elif event == '-DIARIZATION-START-':
            window['-OUTPUT-'].update(window['-OUTPUT-'].get() + "Performing speaker diarization... Please wait.\n")

        elif event == '-DIARIZATION-DONE-':
            diarization = values[event]
            result = window['-OUTPUT-'].get() + "Diarization:\n"
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                result += f"Speaker {speaker}: {turn.start:.2f} - {turn.end:.2f}\n"
            window['-OUTPUT-'].update(result)
            window['-PROGRESS-'].update(75)
            window.write_event_value('-PROCESS-COMPLETE-', None)

        elif event == '-PROCESS-COMPLETE-':
            output_file = values['-OUTPUT-'] or "transcription.html"
            save_to_html(transcription, diarization if values['-DIARIZE-'] else None, output_file)
            window['-PROGRESS-'].update(100)
            sg.popup(f"Transcription saved to {output_file}")

        elif event == '-ERROR-':
            error_message = values[event]
            sg.popup_error(error_message)

        # Update live transcription
        if live_transcriber.is_recording:
            window['-LIVE-OUTPUT-'].update(live_transcriber.get_transcription())

    window.close()

if __name__ == "__main__":
    create_gui()
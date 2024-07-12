from jinja2 import Template

def save_to_html(transcription, diarization, output_file):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Audio Transcription</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
            h2 { color: #2980b9; margin-top: 30px; }
            .speaker { color: #16a085; font-weight: bold; }
            .timestamp { color: #7f8c8d; font-size: 0.9em; }
            .transcription { background-color: #ecf0f1; padding: 15px; border-radius: 5px; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>Audio Transcription</h1>
        
        {% if diarization %}
        <h2>Speaker Diarization</h2>
        <div id="diarization">
            {% for turn in diarization %}
            <p>
                <span class="speaker">Speaker {{ turn.speaker }}:</span>
                <span class="timestamp">{{ turn.start }} - {{ turn.end }}</span>
            </p>
            {% endfor %}
        </div>
        {% endif %}
        
        <h2>Full Transcription</h2>
        <div class="transcription">{{ transcription }}</div>
    </body>
    </html>
    """
    
    diarization_data = []
    if diarization:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            diarization_data.append({
                "speaker": speaker,
                "start": f"{turn.start:.2f}",
                "end": f"{turn.end:.2f}"
            })
    
    template = Template(html_template)
    html_content = template.render(transcription=transcription, diarization=diarization_data)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
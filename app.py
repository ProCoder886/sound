from flask import Flask, render_template, request, send_file, abort
import os
from elevenlabs.client import ElevenLabs

# Get API key from environment variable
api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    raise Exception("ELEVENLABS_API_KEY environment variable not set!")

# Initialize ElevenLabs API
elevenlabs = ElevenLabs(api_key=api_key)

app = Flask(__name__)

# Generate sound effect function
def generate_sound_effect(text: str, output_path: str):
    result = elevenlabs.text_to_sound_effects.convert(
        text=text,
        duration_seconds=4,  # Optional, can be removed to automatically determine length
        prompt_influence=0.5  # Optional
    )

    with open(output_path, "wb") as f:
        for chunk in result:
            f.write(chunk)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle sound effect generation
@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt')
    output_file = "output.mp3"
    
    if not prompt:
        return abort(400, "Prompt is required")
    
    generate_sound_effect(prompt, output_file)
    
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

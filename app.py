from flask import Flask, request, send_file, render_template_string, abort
import os
from elevenlabs.client import ElevenLabs

# Get API key from environment variable
api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    raise Exception("ELEVENLABS_API_KEY environment variable not set!")

# Initialize ElevenLabs API
elevenlabs = ElevenLabs(api_key=api_key)

app = Flask(__name__)

# HTML content from index.html
HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Sound Effect Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        input {
            width: 80%;
            padding: 10px;
            margin: 10px 0;
        }
        button {
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Generate AI Sound Effect</h1>
        <form action="/generate" method="post">
            <label for="prompt">Enter a prompt for the sound effect:</label>
            <input type="text" id="prompt" name="prompt" required>
            <button type="submit">Generate</button>
        </form>
    </div>
</body>
</html>
'''

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
    return render_template_string(HTML_CONTENT)

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

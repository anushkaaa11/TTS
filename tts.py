from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from gtts import gTTS
import os
import time

app = Flask(__name__)
CORS(app)

# Define the static folder for saving the generated MP3 files
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/')
def home():
    return render_template('tts.html')

@app.route('/text-to-speech', methods=['GET', 'POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Generate the text-to-speech audio file
        tts = gTTS(text=text, lang='en')
        filename = f"speech_{int(time.time())}.mp3"  # Unique filename using a timestamp
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        tts.save(filepath)

        # Return the path to the generated speech file
        return jsonify({"speech_url": f"/{filepath}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask, request, jsonify, render_template
import sounddevice as sd
import numpy as np
import speech_recognition as sr

app = Flask(__name__)

# List available audio devices at startup for debugging.
print("Available audio devices:")
print(sd.query_devices())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    # Configuration for audio recording
    duration = 5# seconds
    samplerate = 44100  # Sample rate (Hz)
    device_index = None  # Automatically use the default device
    try:
        # Record audio
        print("Listening...")
        recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16', device=device_index)
        sd.wait()

        # Flatten the recorded audio data and find its max amplitude
        audio_data = np.int16(recording.flatten())
        max_amplitude = np.max(np.abs(audio_data))
        print(f"Max Amplitude: {max_amplitude}")

        # Convert recorded data into audio data compatible with SpeechRecognition
        recognizer = sr.Recognizer()
        audio = sr.AudioData(audio_data.tobytes(), samplerate, 2)  # '2' indicates 16-bit audio data

        # Perform speech recognition
        print("Processing audio...")
        original_text = recognizer.recognize_google(audio)
        print("Original Text:", original_text)

        # Simulate enhanced text logic (replace this with actual enhancement if required)
        enhanced_text = f"{original_text} (Enhanced)"
        print("Enhanced Text:", enhanced_text)

        # Return JSON response
        return jsonify({"original": original_text, "enhanced": enhanced_text})

    except sr.UnknownValueError:
        # Handle cases where speech is not recognized
        print("Speech not recognized.")
        return jsonify({"original": "Speech not recognized. Please try again.", "enhanced": "N/A"})

    except Exception as e:
        # Handle any unexpected errors
        error_message = f"Error: An unexpected error occurred. {e}"
        print(error_message)
        return jsonify({"original": error_message, "enhanced": "N/A"})

if __name__ == '__main__':
    # Ensure debug mode is enabled for easier troubleshooting during development
    app.run(debug=True)

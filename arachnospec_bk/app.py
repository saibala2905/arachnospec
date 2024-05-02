# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from main import process_youtube_video  # Assuming this function is correctly set up to return the transcript path
# app = Flask(__name__)
# CORS(app)  # Enable CORS

# @app.route('/process_video', methods=['POST'])
# def process_video():
#     url = request.json['url']
#     try:
#         transcript_path = process_youtube_video(url)
        
#     except Exception as e:
#         print(e)
#         return jsonify({"error": str(e)}), 500

# @app.route('/chat', methods=['POST'])
# def chat():
#     # Assuming convo is stored and retrieved from a suitable place like session
#     user_message = request.json['message']
#     try:
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from main import process_youtube_video  # Assuming this processes the video and returns the path of an audio file
import google.generativeai as genai
import hashlib
from pathlib import Path

# Configure your API
genai.configure(api_key="AIzaSyDer7eV4AVDf1uclgeGhBJKoFX-6_bjWys")
app = Flask(__name__)
CORS(app)  # Enable CORS

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config={
                                  "temperature": 1,
                                  "top_p": 0.95,
                                  "top_k": 0,
                                  "max_output_tokens": 8192
                              },
                              system_instruction="Use uploaded audio to answer the user prompts. \n Keep responses precise and to the point.\nClear user prompts by denoting the essential key frames from the video.",
                              safety_settings=[
                                  {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
                              ])

your_file = None
@app.route('/process_video', methods=['POST'])
def process_video():
    global your_file
    url = request.json['url']
    try:
        audio_path = process_youtube_video(url)  # Process video and extract audio to file
        your_file = genai.upload_file(path=audio_path)
        return jsonify({"message": "Video processed and chat session started"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    try:
        print(user_message)
        response = model.generate_content([user_message, your_file])
        response_text = response.text
        return jsonify({"message": response_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

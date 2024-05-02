"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from pathlib import Path
import hashlib
import google.generativeai as genai
from IPython.display import Markdown

genai.configure(api_key="AIzaSyDer7eV4AVDf1uclgeGhBJKoFX-6_bjWys")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

sample_file = genai.upload_file(path="C:\PERSONAL\Hackathon\codeImage.png",
                            display_name="freecodecamp setup")

print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

response = model.generate_content(["Extract the code from the image.", sample_file])

print(response)

Markdown(">" + response.text)
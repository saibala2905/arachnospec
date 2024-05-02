import google.generativeai as genai
import json

# Configure the API key for Google's Generative AI
genai.configure(api_key="AIzaSyDer7eV4AVDf1uclgeGhBJKoFX-6_bjWys")

def save_transcript_from_string(transcript_string, output_filename="transcript.txt"):
    try:
        # Save the plain text transcript to a file
        with open(output_filename+"_transcript.txt", 'w') as outfile:
            outfile.write(transcript_string)

        print("Transcript saved successfully to", output_filename)
        return True

    except Exception as e:
        print("An error occurred while saving the transcript:", e)
        return False


def generate_transcript_with_timestamps(audio_path,title):
    try:
        # Upload the audio file to Google's API
        sample_file = genai.upload_file(path=audio_path, display_name=audio_path.split('/')[-1])
        print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

        # Initialize the model
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

        # Generate transcript with timestamps
        response = model.generate_content(["Perform speech to text and also include transcript with timestamp which can be saved and used again to answer further questions.", sample_file])

        # Print and return the transcript response as JSON
        print("Transcript and timestamps generated successfully.")
        
        print(response.text)

        # Save the JSON response to a file
        return save_transcript_from_string(response.text,title)

    except Exception as e:
        print("An error occurred while generating the transcript:", e)
        return None


from pydub import AudioSegment
import google.generativeai as genai
import os
import concurrent.futures

def save_transcript_from_string(transcript_string, output_filename="transcript.txt"):
    try:
        # Save the plain text transcript to a file
        with open(output_filename + "_transcript.txt", 'w') as outfile:
            outfile.write(transcript_string)
        print("Transcript saved successfully to", output_filename)
        return output_filename+"_transcript.txt"
    except Exception as e:
        print("An error occurred while saving the transcript:", e)
        return False

genai.configure(api_key="AIzaSyDer7eV4AVDf1uclgeGhBJKoFX-6_bjWys")

def split_audio(audio_path, segment_length_ms=120000):  # 60 seconds per chunk
    audio = AudioSegment.from_file(audio_path)
    length_audio = len(audio)
    chunks = [audio[i:i + segment_length_ms] for i in range(0, length_audio, segment_length_ms)]
    return chunks

def save_chunks(chunks, base_path):
    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_filename = f"{base_path}_chunk{i}.wav"
        chunk.export(chunk_filename, format="wav")
        chunk_files.append(chunk_filename)
    return chunk_files

def transcribe_chunk(file, model):
    try:
        # Upload and transcribe as before
        sample_file = genai.upload_file(path=file, display_name=file.split('/')[-1])
        response = model.generate_content(["Transcribe this audio.", sample_file])
        os.remove(file)  # Optionally remove the chunk file after processing
        return response.text
    except Exception as e:
        print(f"Failed to process {file}: {e}")
        return None

def transcribe_chunks(chunk_files, model):
    transcripts = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit all transcription tasks to the executor
        future_to_file = {executor.submit(transcribe_chunk, file, model): file for file in chunk_files}
        for future in concurrent.futures.as_completed(future_to_file):
            result = future.result()
            if result:
                transcripts.append(result)
    return transcripts

def combine_transcripts(transcripts):
    # Combine the transcripts while handling timestamps
    full_transcript = " ".join(transcripts)
    return full_transcript

def generate_transcript_for_large_files(audio_path, title):
    try:
        # Split audio into chunks
        chunks = split_audio(audio_path)
        chunk_files = save_chunks(chunks, os.path.splitext(audio_path)[0])
        
        # Initialize the model
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

        # Transcribe each chunk in parallel
        transcripts = transcribe_chunks(chunk_files, model)
        
        # Combine transcripts
        full_transcript = combine_transcripts(transcripts)
        
        # Save to a file
        return save_transcript_from_string(full_transcript, title)

    except Exception as e:
        print("An error occurred:", e)
        return None

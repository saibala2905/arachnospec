from pathlib import Path
import hashlib
import google.generativeai as genai

# Configure the API and the model
def setup_model(api_key):
    genai.configure(api_key=api_key)
    
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }
    
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]
    
    system_instruction = "From the uploaded audio create a time stamp based transcript.\nUse that transcript to answer the user prompts.\nClear user prompts by denoting the essential key frames from the video."

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                  generation_config=generation_config,
                                  system_instruction=system_instruction,
                                  safety_settings=safety_settings)
    return model

def upload_if_needed(pathname: str, uploaded_files: list):
    path = Path(pathname)
    if not path.exists():
        print(f"Error: The file {pathname} does not exist.")
        return []
    
    hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
    try:
        existing_file = genai.get_file(name=hash_id)
        return [existing_file.uri]
    except:
        pass
    
    uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
    return [uploaded_files[-1].uri]

def upload_file(pathname: str, uploaded_files: list):
    path = Path(pathname)
    if not path.exists():
        print(f"Error: The file {pathname} does not exist.")
        return []
    
    # Upload the file
    hash_id = hashlib.sha256(path.read_bytes()).hexdigest()  # Optional: generate a unique ID using hash
    uploaded_file = genai.upload_file(path=path, display_name=hash_id)
    print(upload_file.uri)
    uploaded_files.append(upload_file.uri)
    
    return [uploaded_files[-1].uri]

def manage_chat_session(model, file_path):
    uploaded_files = []
    file_uri = upload_if_needed(file_path, uploaded_files)
    if not file_uri:
        print("Failed to upload file.")
        return
    
    convo = model.start_chat(history=[])
    
    while True:
        user_input = input("Enter your question (type 'exit' to end): ")
        if user_input.lower() == 'exit':
            break
        convo.send_message(user_input)
        print(convo.last.text)

    for uploaded_file in uploaded_files:
        genai.delete_file(name=uploaded_file.name)

def chat(file_path):
    api_key="AIzaSyDer7eV4AVDf1uclgeGhBJKoFX-6_bjWys"
    model = setup_model(api_key)
    manage_chat_session(model, file_path)


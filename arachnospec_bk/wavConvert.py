import noisereduce as nr
from pydub import AudioSegment
import numpy as np

# def convert_to_wav(source_path):
#     try:
#         # Load the source audio file
#         audio = AudioSegment.from_file(source_path)

#         # Check if the audio is stereo (2 channels) and convert it to mono
#         if audio.channels > 1:
#             audio = audio.set_channels(1)

#         # Define the output path with the same base filename but with .wav extension
#         output_path = source_path.rsplit('.', 1)[0] + ".wav"

#         # Export the file as WAV in mono
#         audio.export(output_path, format="wav")

#         # Print successful conversion message
#         print("Converted successfully to:", output_path)
#         return output_path

#     except Exception as e:
#         # Print an error message if something goes wrong
#         print("Failed to convert to WAV:", e)
#         return None

# def convert_to_wav_and_denoise(source_path):
#     try:
#         # Load the source audio file
#         audio = AudioSegment.from_file(source_path)

#         # Convert to mono if stereo
#         if audio.channels > 1:
#             audio = audio.set_channels(1)

#         # Convert AudioSegment to numpy array
#         audio_np = np.array(audio.get_array_of_samples())

#         # Perform noise reduction
#         reduced_noise_audio_np = nr.reduce_noise(y=audio_np, sr=audio.sample_width * audio.frame_rate)

#         # Convert the numpy array back to AudioSegment
#         reduced_noise_audio = audio._spawn(reduced_noise_audio_np)

#         # Define the output path with .wav extension
#         output_path = source_path.rsplit('.', 1)[0] + ".wav"

#         # Export the file as WAV
#         reduced_noise_audio.export(output_path, format="wav")

#         print("Converted and noise-reduced successfully to:", output_path)
#         return output_path

#     except Exception as e:
#         print("Failed to convert and reduce noise:", e)
#         return None

import noisereduce as nr
from pydub import AudioSegment
import numpy as np

def convert_to_wav_and_denoise(source_path, target_sample_rate=4000, bit_depth=8):
    try:
        # Load the source audio file
        audio = AudioSegment.from_file(source_path)

        # Convert to mono if stereo
        if audio.channels > 1:
            audio = audio.set_channels(1)

        # Reduce sample rate and bit depth
        audio = audio.set_frame_rate(target_sample_rate)
        audio = audio.set_sample_width(bit_depth // 8)

        # Convert AudioSegment to numpy array
        audio_np = np.array(audio.get_array_of_samples())

        # Perform noise reduction
        reduced_noise_audio_np = nr.reduce_noise(y=audio_np, sr=audio.frame_rate)

        # Convert the numpy array back to AudioSegment
        reduced_noise_audio = audio._spawn(reduced_noise_audio_np)

        # Define the output path with .wav extension
        output_path = source_path.rsplit('.', 1)[0] + ".wav"

        # Export the file as WAV
        reduced_noise_audio.export(output_path, format="wav")

        print("Converted and noise-reduced successfully to:", output_path)
        return output_path

    except Exception as e:
        print("Failed to convert and reduce noise:", e)
        return None

import noisereduce as nr
from pydub import AudioSegment
import numpy as np

def convert_to_m4a_and_denoise(source_path, target_sample_rate=8000, bit_depth=8, target_bitrate="32k"):
    try:
        # Load the source audio file
        audio = AudioSegment.from_file(source_path)

        # Convert to mono if stereo
        if audio.channels > 1:
            audio = audio.set_channels(1)

        # Reduce sample rate and bit depth
        audio = audio.set_frame_rate(target_sample_rate)
        audio = audio.set_sample_width(bit_depth // 8)

        # Convert AudioSegment to numpy array for denoising
        audio_np = np.array(audio.get_array_of_samples())
        sr = audio.frame_rate

        # Perform noise reduction
        reduced_noise_audio_np = nr.reduce_noise(y=audio_np, sr=sr)

        # Convert the numpy array back to AudioSegment
        reduced_noise_audio = audio._spawn(reduced_noise_audio_np)

        # Define the output path with .m4a extension
        output_path = source_path.rsplit('.', 1)[0] + ".m4a"

        # Export the file as M4A
        reduced_noise_audio.export(output_path, format="ipod", bitrate=target_bitrate)

        print("Converted and noise-reduced successfully to M4A:", output_path)
        return output_path

    except Exception as e:
        print("Failed to convert and reduce noise:", e)
        return None

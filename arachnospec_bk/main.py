# from pytube import YouTube
# from wavConvert import convert_to_wav
# from chatSession import chat
# from getTranscriptChunks import generate_transcript_for_large_files
# import re

# # Video URL link from user.
# ytbLink = input("Enter URL: ")
# print("Video Link", ytbLink)

# def extract_video_id(url):
#     # This regex pattern is designed to match and extract the video ID from YouTube URLs
#     youtube_regex = (
#         r'(https?://)?(www\.)?'
#         '(youtube|youtu|youtube-nocookie)\.(com|be)/'
#         '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
#     )
#     youtube_regex_match = re.match(youtube_regex, url)
#     if youtube_regex_match:
#         return youtube_regex_match.group(6)
#     return None

# ytId = extract_video_id(ytbLink)
# #Youtube video object.
# yt = YouTube(ytbLink)

# #Print some details related to youtube video
# print("Video ID", ytId)
# print("Title:", yt.title)
# print("Number of views:", yt.views)
# print("Length of video (seconds):", yt.length)
# print("Rating of video:", yt.rating)
# print(yt.title)

# # Check if a transcript is available
# if yt.captions:
#     print("Transcript is available.")
# else:
#     print("Transcript is not available.")

# ytAudStream = yt.streams.filter(only_audio=True).first()

# try:
#     # Select the audio stream
#     ytAudStream = yt.streams.get_audio_only()

#     # Download the audio file
#     output_path = ytAudStream.download(output_path=".", filename=ytId+".mp3")

#     # Print confirmation message
#     print("File successfully downloaded:", output_path)

# except Exception as e:
#     # Print the error
#     print("An error occurred:", e)
    
    
# convert_to_wav(output_path)

# # generate_transcript_with_timestamps(ytId+".wav",ytId)

# # generate_transcript_for_large_files(ytId+".wav",ytId)

# # chat(ytId+"_transcript.txt")

from pytube import YouTube
from wavConvert import convert_to_wav_and_denoise
from aacConvert import convert_to_m4a_and_denoise
from chatSession import chat
from getTranscriptChunks import generate_transcript_for_large_files
import re

def process_youtube_video(url):
    print("Video Link", url)

    def extract_video_id(url):
        # This regex pattern is designed to match and extract the video ID from YouTube URLs
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        youtube_regex_match = re.match(youtube_regex, url)
        if youtube_regex_match:
            return youtube_regex_match.group(6)
        return None

    ytId = extract_video_id(url)
    if not ytId:
        print("Invalid YouTube URL")
        return

    yt = YouTube(url)

    # Print some details related to youtube video
    print("Video ID:", ytId)
    print("Title:", yt.title)
    print("Number of views:", yt.views)
    print("Length of video (seconds):", yt.length)
    print("Rating of video:", yt.rating)

    # Check if a transcript is available
    if yt.captions:
        print("Transcript is available.")
    else:
        print("Transcript is not available.")

    try:
        # Select the audio stream and download the audio file
        ytAudStream = yt.streams.get_audio_only()
        output_path = ytAudStream.download(output_path=".", filename=ytId + ".mp3")
        print("File successfully downloaded:", output_path)
    except Exception as e:
        print("An error occurred:", e)
        return

    # Convert audio to WAV format
    # wav_path = convert_to_wav_and_denoise(output_path)
    # aac_path = convert_to_aac_and_denoise(output_path)
    m4a_path = convert_to_m4a_and_denoise(output_path)

    # Generate transcript
    # transcript_path = generate_transcript_for_large_files(m4a_path, ytId)

    # Start chat session based on the transcript
    # chat(transcript_path)
    
    return m4a_path

# Example usage:
# process_youtube_video("https://www.youtube.com/watch?v=example")

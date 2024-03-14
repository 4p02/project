import yt_dlp  # Import yt-dlp for downloading video subtitles
import re  # Import re for regular expression operations
import os  # Import os for interacting with the operating system
from llama import Llama
import asyncio





def download_video_with_subtitles(url):
    # Download subtitles for a YouTube video using yt-dlp
    ydl_opts = {
        'writeautomaticsub': True,  # Enable automatic subtitle download
        'subtitlesformat': 'vtt',  # Set subtitle format to VTT
        'skip_download': True  # Skip downloading the video itself
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    # Search for the downloaded VTT file in the current directory
    for file in os.listdir('.'):
        if file.endswith('.en.vtt'):
            return file  # Return the path to the VTT file
    return None  # Return None if no file was found



def process_webvtt(file_path):
    # Clean the VTT file by removing timestamps and unnecessary whitespace
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Remove timestamps and formatting tags from the VTT content
    content = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}><c>[^<]+</c>', '', content)
    content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*\n', '', content)
    content = re.sub(r'\n\s*\n', '\n', content)
    return content  # Return the cleaned content



def delete_file(file_path):
    # Delete a file at the given path
    if os.path.exists(file_path):
        os.remove(file_path)  # Remove the file if it exists





async def summarize_video(video_url):
    # Connect to Llama
    llama_client = await Llama.connect()

    # Download the video subtitles as before
    vtt_file_path = download_video_with_subtitles(video_url)
    if vtt_file_path:
        processed_content = process_webvtt(vtt_file_path)  # Process the VTT file to clean it
        summarized_content = processed_content[:8000]  # Limit the content size to 8000 characters

        # Use Llama for summarization
        summary_response = await llama_client.chat(
            messages=[{"role": "user", "content": f"print 1"}]
        )
        summary = summary_response.messages[-1].content

        delete_file(vtt_file_path)  # Delete the temporary VTT file
        return summary  # Return the video summary
    else:
        return "Subtitle file could not be downloaded or found."


async def test_ollama_question():
    llama_client = await Llama.connect()
    question = "What is 1+1?"
    response = await llama_client.chat(messages=[{"role": "user", "content": question}])
    answer = response.messages[-1].content
    return answer


async def main():
    video_url = "https://youtu.be/_IS2SetIpOU?si=iRo1BAlpetmHiKVw"  # Video URL to summarize
    # summary_task = summarize_video(video_url)
    answer = await test_ollama_question()
    print(f"Answer to 'What is 1+1?': {answer}")




if __name__ == "__main__":
    asyncio.run(main())


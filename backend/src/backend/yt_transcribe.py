import yt_dlp  # Import yt-dlp for downloading video subtitles
import re  # Import re for regular expression operations
import os  # Import os for interacting with the operating system
import openai  # Import the OpenAI library for accessing GPT-4

def initialize_openai_client():
    # Initialize the OpenAI client using the API key from environment variables
    return openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

def summarize_text_with_gpt4(client, text):
    # Summarize the given text using OpenAI's GPT-4 model
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize this video for me: \n{text}",
                }
            ],
            model="gpt-4-0125-preview",
        )
        return response.choices[0].message.content  # Return the summary content
    except Exception as e:
        return str(e)  # Return the error message if an exception occurs

def summarize_video(video_url):
    # Main function to download, process, and summarize video subtitles
    client = initialize_openai_client()  # Initialize the OpenAI client
    vtt_file_path = download_video_with_subtitles(video_url)  # Download the video subtitles
    if vtt_file_path:
        processed_content = process_webvtt(vtt_file_path)  # Process the VTT file to clean it
        summarized_content = processed_content[:8000]  # Limit the content size to 8000 characters
        summary = summarize_text_with_gpt4(client, summarized_content)  # Get the summary from GPT-4
        delete_file(vtt_file_path)  # Delete the temporary VTT file
        return summary  # Return the video summary
    else:
        return "Subtitle file could not be downloaded or found."  # Return error message if no subtitles found

if __name__ == "__main__":
    # This block executes if the script is run directly (not imported as a module)
    video_url = "https://youtu.be/_IS2SetIpOU?si=iRo1BAlpetmHiKVw"  # Video URL to summarize
    summary = summarize_video(video_url)  # Perform the video summarization
    print(summary)  # Print the obtained summary

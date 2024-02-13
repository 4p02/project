import yt_dlp
import re
import os
from openai import OpenAI


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

video_url = "https://youtu.be/AF8d72mA41M?si=0jXJqFFhmhF_tATl"  # Replace with the URL of the video you want to download




def download_video_with_subtitles(url):
    ydl_opts = {
        'writeautomaticsub': True,   # Write the automatic subtitles to a separate file
        'subtitlesformat': 'vtt',   # Specify the subtitle format as VTT
        'skip_download': True     # Do not download the video
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    # Find the path of the downloaded VTT file
    for file in os.listdir('.'):
        if file.endswith('.en.vtt'):
            return file
    return None

def process_webvtt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    content = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}><c>[^<]+</c>', '', content)
    content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*\n', '', content)
    content = re.sub(r'\n\s*\n', '\n', content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def delete_file(file_path):
    input("Press any key to delete the subtitle file...")
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted.")
    else:
        print(f"File '{file_path}' not found.")

def vtt_to_string(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    vtt_file_path = download_video_with_subtitles(video_url)
    if vtt_file_path:
        process_webvtt(vtt_file_path)
        vtt_content = vtt_to_string(vtt_file_path)
        summarized_content = vtt_content[:8000]
        chat_completion = client.chat.completions.create(
        messages=[
            {
            "role": "user",
            "content": f"Summarize this video for me: \n{summarized_content}",
            }
            ],
        model="gpt-4-0125-preview",
                        )
        print(chat_completion.choices[0].message.content)
        delete_file(vtt_file_path)


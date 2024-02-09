import subprocess

## the path has to be changed to that of not my machine, this is not working properly but it does connect to yt and downloads a transcript,

# Full path to the yt-dlp executable
yt_dlp_path = "C:\\Users\\joseh\\Documents\\YT-DLP\\yt-dlp.exe"

# URL of the YouTube video you want to transcribe
video_url = "https://www.youtube.com/watch?v=cD5T1Y4b7wA&list=RDMMQlZNGcVfeF0&index=4&ab_channel=FeidVEVO"

# Command to transcribe the YouTube video using yt-dlp
command = [yt_dlp_path, "--write-sub", "--sub-lang", "es", "--skip-download", "--convert-subs", "srt", "-o", "-", video_url]

# Execute the command and print the output to see if it works
try:
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    transcription = result.stdout
    print("Transcription:")
    print(transcription)
except subprocess.CalledProcessError as e:
    print("Error:", e)

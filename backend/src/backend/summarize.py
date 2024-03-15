


class Summerize:
    def __init__(self, url, user):
        pass
    def summerize_article(self):
        pass
    def save_to_database(self):
        pass
    
    def summerize_video(self):
        pass

def summary_prompt(text: str) -> str:
    return f"Take a deep breath and summarize the following text:\n{text}"



def video_recursive_summary_prompt(text: str, summary_history: str = "") -> str:
    """
    Generates the prompt for recursive prompt-based moving/expanding context window summarization for videos

    Please use only when context window is too small for transcript size.
    """
    prompt = f"Below is a part of the transcript of the video that has yet to be summarized:\n{text}\n\nSummarize this transcript"
    if len(summary_history) != 0:
        prompt = f"Below is the summary of the video so far, please keep this summary in mind when summarizing following parts of the video:\n{summary_history}\n\n" + prompt + " while keeping the summary of the video so far in mind"
    prompt += ":"
    return prompt
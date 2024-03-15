


class Summerize:
    
    

    def __init__(self, url, user):
        pass
    def summerize_article(self):
        pass
    def save_to_database(self):
        pass
    
    def summerize_video(self):
        pass



def summary_prompt(text: str, is_completion: bool = False) -> str:
    prompt = f"Take a deep breath and summarize the following text:\n{text}"
    return prompt if not is_completion else prompt+"\n\nSummary:"

def video_recursive_summary_prompt(text: str, summary_history: str = "", is_completion: bool = False) -> str:
    """
    Generates the prompt for recursive prompt-based moving/expanding context window summarization for videos

    Please use only when context window is too small for transcript size.
    """
    prompt = f"Below is a part of the transcript of the video that has yet to be summarized:\n{text}\n\nSummarize this transcript"
    if len(summary_history) != 0:
        prompt = f"Below is the summary of the video so far, please keep this summary in mind when summarizing following parts of the video:\n{summary_history}\n\n" + prompt + " while keeping the summary of the video so far in mind"
    return prompt+":" if not is_completion else prompt+".\n\nSummary:"


def paragraph_summary_prompt(paragraph: str, is_completion: bool = False) -> str:
    """
    Generates the prompt for summarizing a paragraph into 1-2 sentences

    Use for summarizing individual paragraphs when context window is too small for full article + response
    """
    prompt = f"Summarize the following paragraph:\n{paragraph}"
    return prompt if not is_completion else prompt+"\n\nSummary:"

def combine_paragraph_summaries_prompt(paragraphs: list[str], is_completion: bool = False) -> str:
    """
    Combines multiple paragraphs summaries and summarizes the document

    Used with instances of results from using 'paragraph_summary_prompt()' on an LLM in an ordered list
    """
    prompt = ""
    for summary in paragraphs:
        prompt += summary + "\n\n"
    prompt = prompt[:-2] # Trimming the last \n\n

    return summary_prompt(prompt, is_completion)
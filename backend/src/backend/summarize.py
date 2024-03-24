from backend.db import Database
from bs4 import BeautifulSoup
from backend.llama import Llama
from backend.auth import create_document
from backend.misc import bytes_to_str, str_to_bytes
class Summerize:
    
    

    def __init__(self, url, user):
        pass
    def summerize_article(self):
        pass
    def save_to_database(self):
        pass
    
    def summerize_video(self):
        pass


def parse_article(url: str, db: Database):
    """
    TODO: Pre prompting
    headers, body, meta, article, section, main, img alt tag, a, p, li, ol, ul, img, figcaption, table)
    """
    get_html = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Temporary HTML</title>
</head>
<body>

    <header>
        <h1>Header</h1>
    </header>

    <nav>
        <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">Contact</a></li>
        </ul>
    </nav>

    <main>
        <article>
            <h2>Article Title</h2>
            <p>This is the content of the article.</p>
            <figure>
                <img src="image.jpg" alt="Description of the image">
                <figcaption>Figure caption goes here</figcaption>
            </figure>
        </article>

        <section>
            <h2>Section Title</h2>
            <p>This is the content of the section.</p>
        </section>

        <aside>
            <h2>Aside Title</h2>
            <p>This is the content of the aside.</p>
        </aside>
    </main>

    <footer>
        <p>Copyright © 2024. All rights reserved.</p>
    </footer>
    <p>TEMPORARY HTML</p>
</body>
</html>
    """
    soup = BeautifulSoup(get_html)
    title = soup.find_all("title")[0].text
    tags_we_want = ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "ol", "ul", "img", "figcaption", "table"]
    total_text = ""
    for tag in soup.find_all(tags_we_want):
        if str(tag.name).startswith("h"):
            print(tag.text)
            total_text += tag.text + "\n"
        elif tag.name == "p":
            print(tag.text)
            total_text += tag.text + "\n"
        elif tag.name == "li":
            print(tag.text)
            total_text += tag.text + "\n"
        elif tag.name == "ol":
            print(tag.text)
            total_text += tag.text + "\n"
        elif tag.name == "ul":
            print(tag.text)
            total_text += tag.text + "\n"
        elif tag.name == "img":
            if "alt" in tag.attrs:
                print(tag["alt"])
                total_text += tag["alt"] + "\n"
        elif tag.name == "figcaption":
            print(tag.text)
            total_text += tag.text + "\n"
        elif tag.name == "table":
            print(tag.text)
            total_text += tag.text + "\n"
    

    sum_prompt = summary_prompt(total_text)
    summary = Llama().chat(messages=[{"role": "system", "content": sum_prompt}])
    created_doc = create_document(db=db, source_url=url, body=str_to_bytes(total_text), summary=str_to_bytes(summary), title=title)
    if created_doc is None:
        print("Line 114 (summarize.py): Document not created successfully")
    return summary

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


if __name__ == "__main__":
    parse_article("https://example.com")
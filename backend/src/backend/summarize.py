from backend.db import Database
from bs4 import BeautifulSoup
from backend.llama import Llama
from backend.auth import create_document
from backend.misc import str_to_bytes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


async def parse_article(url: str, db: Database):
    """
    Get important headers, body, meta, article, section, main, img alt tag, a, p, li, ol, ul, img, figcaption, table) from url
    Use selenium to get the full html of the page
    BeautifulSoup to parse the html
    Extract the text from the tags we want
    Send the text to ollama to summarize
    return the summary and the document id
    """
    # stop the browser from opening up
    options = Options()
    options.add_argument('--headless=new')
    selenium_driver = webdriver.Chrome(options=options)
    selenium_driver.get(url)
    title = selenium_driver.title
    get_html = selenium_driver.execute_script("return document.body.innerHTML")
    print(get_html, "GET_HTML")
    selenium_driver.quit()
    if get_html is None:
        print("Line 57 (summarize.py): get_html is None")
        raise Exception("get_html is None")
    soup = BeautifulSoup(get_html)
    tags_we_want = ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "ol", "ul", "img", "code", "figcaption", "table"]
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
    try:
        llama_client = await Llama.connect()
        summary_response = await llama_client.generate(prompt=sum_prompt, model="mistral:7b-instruct-v0.2-q4_K_M")
        summary = summary_response.messages[-1].content
    except Exception as e:
        print(f"Line 66 (summarize.py): {e}")
        print("prob connection to ollama")
        raise e

    created_doc = await create_document(db=db, source_url=url, body=str_to_bytes(total_text), summary=str_to_bytes(summary), title=title)
    if created_doc is None:
        print("Line 114 (summarize.py): Document not created successfully")
        raise Exception("Document not created successfully")
    return summary, created_doc["id"]

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
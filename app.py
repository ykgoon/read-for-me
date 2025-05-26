import os

import google.generativeai as genai
from curl_cffi import requests
from flask import Flask, request, send_file
from flask_cors import CORS
from markdown import markdown
from readability import Document
from urllib.parse import urlparse

from youtube import YouTube

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')


@app.route('/summarize', methods=['GET'])
async def summarize(is_news=False):
    url = request.args.get('url')
    try:
        parsed_original_url = urlparse(url)
        archive_domains = [
            "ft.com",
            "bloomberg.com",
            "washingtonpost.com",
            "nytimes.com",
            "wired.com",
            "404media.co",
            "politico.com",
            "economist.com",
            "thediplomat.com",
        ]
        if any(parsed_original_url.netloc.endswith(domain) for domain in archive_domains):
            archive_submit_url = "https://archive.is/submit/"
            app.logger.info(f"Attempting to fetch URL {url} (domain: {parsed_original_url.netloc}) via archive.is")

            # Make a POST request to archive.is.
            # curl_cffi's post method follows redirects by default.
            response = requests.post(
                archive_submit_url,
                data={"url": url},
                impersonate="chrome",  # Mimic a browser
                timeout=60  # Add a timeout
            )
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

            # The final URL after redirects is the snapshot URL
            snapshot_url = response.url
            app.logger.info(f"Using archive.is snapshot URL: {snapshot_url}")
            url = snapshot_url  # Update the URL to use the snapshot

    except requests.RequestsError as e:
        # Log the error and continue with the original URL as a fallback
        app.logger.error(f"Failed to get snapshot from archive.is for {url}: {e}. Proceeding with original URL.")
    except Exception as e:
        # Catch any other unexpected errors (e.g., during URL parsing)
        app.logger.error(f"An unexpected error occurred while trying to process {url} with archive.is: {e}. Proceeding with original URL.")

    yt = YouTube()
    if yt.is_link(url):
        content = yt.get_transcriptions(url)
        if not content:
            return f'''
            <html><body><content>
              Could not transcribe YouTube video.
            </content></body></html>
            '''

    else:
        html_content = requests.get(url, impersonate="chrome").text
        content = Document(html_content).summary()

    prompt_file = "prompts/article.md"
    if is_news: prompt_file = "prompts/news.md"
    with open(prompt_file) as f:
        system_instruction = f.read()

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        'gemini-2.5-flash-preview-05-20',
        system_instruction=system_instruction,
    )
    response = model.generate_content(content)
    return f'''
    <html><body><article>
        {markdown(response.text)}
    </article></body></html>
    '''

@app.route('/news', methods=['GET'])
async def news():
    return await summarize(is_news=True)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=os.environ.get("DEBUG") == '1'
    )

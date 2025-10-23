import json
import os
import logging

from curl_cffi import requests
from flask import Flask, redirect, request, send_file
from flask_cors import CORS
from markdown import markdown
from readability import Document
from urllib.parse import urlparse

from youtube import YouTube

app = Flask(__name__)
CORS(app)

app.logger.setLevel(logging.ERROR)

@app.route('/')
def index():
    return send_file('index.html')


@app.route('/summarize', methods=['GET'])
async def summarize(is_news=False):
    url = request.args.get('url')

    parsed_original_url = urlparse(url)
    with open('archive_domains.json') as f:
        archive_domains = json.load(f)
    if any(parsed_original_url.netloc.endswith(domain) for domain in archive_domains):
        app.logger.info(f"Attempting to fetch URL {url} (domain: {parsed_original_url.netloc}) via archive.is")
        url = f"https://archive.is/newest/{url}"
        return redirect(url, code=302)

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

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY environment variable is not set", 500

    api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
    model_name = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": content}
        ]
    }
    try:
        response = requests.post(
            f"{api_base}/chat/completions",
            json=payload,
            headers=headers,
            timeout=60,
            stream=True,
        )
        response.raise_for_status()

        # Collect the streamed response
        response_data = ""
        for chunk in response.iter_lines():
            if chunk:
                response_data += chunk.decode('utf-8')

        # Parse the complete response
        response_json = json.loads(response_data)
        text_response = response_json['choices'][0]['message']['content']
    except Exception as e:
        app.logger.error(f"Error calling OpenAI API: {e}")
        return f"An error occurred while generating the summary. {e}", 500

    html_article = markdown(text_response)
    app.logger.debug(f"Markdown: {text_response}")
    app.logger.debug(f"HTML: {html_article}")

    return f'''
    <html><body><article>
        {html_article}
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

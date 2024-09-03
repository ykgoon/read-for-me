import os
import requests

import google.generativeai as genai
from flask import Flask, request, send_file
from flask_cors import CORS
from markdown import markdown
from readability import Document

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')


@app.route('/summarize', methods=['GET'])
async def summarize():
    url = request.args.get('url')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    html_content = requests.get(url, headers=headers).text
    content = Document(html_content)

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    with open("system_prompt.md") as f:
        system_instruction = f.read()
    model = genai.GenerativeModel(
        'gemini-1.5-flash',
        system_instruction=system_instruction,
    )
    response = model.generate_content(content.summary())
    return f'''
    <html><body><content>
        {markdown(response.text)}
    </content></body></html>
    '''

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=os.environ.get("DEBUG") == '1'
    )

import os

import google.generativeai as genai
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from playwright.async_api import async_playwright

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')


@app.route('/summarize', methods=['GET'])
async def summarize():
    url = request.args.get('url')
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await page.goto(url)
        content = await page.evaluate('''
        async () => {
            const readabilityScript = document.createElement('script');
            readabilityScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/readability/0.5.0/Readability.min.js';
            document.head.appendChild(readabilityScript);
            await new Promise(resolve => readabilityScript.onload = resolve);
            const article = new Readability(document).parse();
            return article.textContent;
        }
        ''')
        await browser.close()

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    with open("system_prompt.md") as f:
        system_instruction = f.read()
    model = genai.GenerativeModel(
        'gemini-1.5-flash',
        system_instruction=system_instruction,
    )
    response = model.generate_content(content)

    return jsonify({'summary': response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

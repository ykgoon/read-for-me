from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from playwright.async_api import async_playwright
import asyncio
import google.generativeai as genai

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
    # Use Google Gemini to summarize content
    summarized_content = genai.summarize(content)
    return jsonify({'summary': summarized_content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

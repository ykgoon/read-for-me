from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from playwright.async_api import async_playwright
import asyncio

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
        content = page.evaluate('''
            const readabilityScript = document.createElement('script');
            readabilityScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/readability/0.1.20/readability.min.js';
            document.head.appendChild(readabilityScript);
            await new Promise(resolve => readabilityScript.onload = resolve);
            const article = new Readability(document).parse();
            return article.textContent;
        ''')
        await browser.close()
    return jsonify({'summary': content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

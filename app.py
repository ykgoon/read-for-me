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
        content = await page.content()
        await browser.close()
    return jsonify({'summary': content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

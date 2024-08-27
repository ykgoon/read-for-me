from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import google.generativeai as palm
from playwright.sync_api import sync_playwright

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/summarize', methods=['GET'])
def summarize():
    url = request.args.get('url')
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        # TODO: Extract article body, clean it, and summarize using Google Gemini
        browser.close()
    return jsonify({'summary': 'Summary of the article'})

if __name__ == '__main__':
    app.run(debug=True)

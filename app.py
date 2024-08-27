from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import google.generativeai as palm
from playwright.sync_api import sync_playwright

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')

import scrapy
from scrapy.crawler import CrawlerProcess

class ArticleSpider(scrapy.Spider):
    name = "article"
    start_urls = [request.args.get('url')]

    def parse(self, response):
        content = response.xpath('//body').get()
        print('CuJWBwTI:', content)
        # TODO: Extract article body, clean it, and summarize using Google Gemini
        return {'content': content}

@app.route('/summarize', methods=['GET'])
def summarize():
    url = request.args.get('url')
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",
    })
    process.crawl(ArticleSpider)
    process.start()
    return jsonify({'summary': 'Summary of the article'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

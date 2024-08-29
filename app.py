import scrapy
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')

class ArticleSpider(scrapy.Spider):
    name = "article"

    def __init__(self, url=None, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        content = response.xpath('//body').get()
        # TODO: Extract article body, clean it, and summarize using Google Gemini
        return {'content': content}

@app.route('/summarize', methods=['GET'])
def summarize():
    url = request.args.get('url')
    runner = CrawlerRunner(settings={
        "LOG_LEVEL": "ERROR",
    })

    @defer.inlineCallbacks
    def crawl():
        crawler = yield runner.crawl(ArticleSpider, url=url)
        reactor.stop()
        defer.returnValue(crawler)

    reactor.callWhenRunning(crawl)
    reactor.run()
    return jsonify({'summary': 'Summary of the article'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

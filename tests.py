import unittest
from app import ArticleSpider
from scrapy.crawler import CrawlerRunner
from scrapy.http import HtmlResponse
from twisted.internet import reactor, defer


class TestCrawler(unittest.TestCase):
    def test_parse(self):
        url = 'https://ykgoon.com'
        body = '<html><body><p>Test content</p></body></html>'
        response = HtmlResponse(url=url, body=body, encoding='utf-8')
        spider = ArticleSpider(url=url)
        result = spider.parse(response)
        self.assertEqual(
            result,
            {'content': '<body><p>Test content</p></body>'}
        )

    def test_crawl(self):
        url = 'https://ykgoon.com'
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

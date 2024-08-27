import unittest
from app import ArticleSpider
from scrapy.crawler import CrawlerProcess
from scrapy.http import HtmlResponse


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
        process = CrawlerProcess(settings={
            "LOG_LEVEL": "ERROR",
        })
        process.crawl(ArticleSpider, url=url)
        process.start()

if __name__ == '__main__':
    unittest.main()

import unittest
from scrapy.http import HtmlResponse
from app import ArticleSpider

class TestArticleSpider(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()

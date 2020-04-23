import unittest
from simplified.scrape.scrape import *
from simplified.scrape import models
from simplified import app

class TestScrape(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def test_jumia(self):
        result = jumia(categ="fashion", url="https://www.jumia.com.ng/category-fashion-by-jumia/", test=True)
        self.assertEqual(result, True)

        result = jumia(categ="health and beauty", url="https://www.jumia.com.ng/health-beauty/", test=True)
        self.assertEqual(result, True)

        result = jumia(categ="home and office", url="https://www.jumia.com.ng/home-office/", test=True)
        self.assertEqual(result, True)

        result = jumia(categ="electronics", url="https://www.jumia.com.ng/electronics/", test=True)
        self.assertEqual(result, True)

        result = jumia(categ="phones and tablets", url="https://www.jumia.com.ng/phones-tablets/", test=True)
        self.assertEqual(result, True)

        result = jumia(categ="computing", url="https://www.jumia.com.ng/computing/", test=True)
        self.assertEqual(result, True)

    def test_konga(self):
        result = konga(categ="fashion", url="https://www.konga.com/category/konga-fashion-1259", test=True)
        self.assertEqual(result, True)

        result = konga(categ="health and beauty", url="https://www.konga.com/category/beauty-health-personal-care-4", test=True)
        self.assertEqual(result, True)

        result = konga(categ="home and office", url="https://www.konga.com/category/home-kitchen-602", test=True)
        self.assertEqual(result, True)

        result = konga(categ="electronics", url="https://www.konga.com/category/electronics-5261", test=True)
        self.assertEqual(result, True)

        result = konga(categ="phones and tablets", url="https://www.konga.com/category/phones-tablets-5294", test=True)
        self.assertEqual(result, True)

        result = konga(categ="computing", url="https://www.konga.com/category/computers-accessories-5227", test=True)
        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()
import unittest
from scrape.scrape import *
import random

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
        result = jumia(categ="fashion", url="https://www.jumia.com.ng/category-fashion-by-jumia/")
        self.assertEqual(result, True)

        result = jumia(categ="health and beauty", url="https://www.jumia.com.ng/health-beauty/")
        self.assertEqual(result, True)

        result = jumia(categ="home and office", url="https://www.jumia.com.ng/home-office/")
        self.assertEqual(result, True)

        result = jumia(categ="electronics", url="https://www.jumia.com.ng/electronics/")
        self.assertEqual(result, True)

        result = jumia(categ="phones and tablets", url="https://www.jumia.com.ng/phones-tablets/")
        self.assertEqual(result, True)

        result = jumia(categ="computing", url="https://www.jumia.com.ng/computing/")
        self.assertEqual(result, True)

    def test_konga(self):
        result = konga(categ="fashion", url="https://www.konga.com/category/konga-fashion-1259")
        self.assertEqual(result, True)

        result = konga(categ="health and beauty", url="https://www.konga.com/category/beauty-health-personal-care-4")
        self.assertEqual(result, True)

        result = konga(categ="home and office", url="https://www.konga.com/category/home-kitchen-602")
        self.assertEqual(result, True)

        result = konga(categ="electronics", url="https://www.konga.com/category/electronics-5261")
        self.assertEqual(result, True)

        result = konga(categ="phones and tablets", url="https://www.konga.com/category/phones-tablets-5294")
        self.assertEqual(result, True)

        result = konga(categ="computing", url="https://www.konga.com/category/computers-accessories-5227")
        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()
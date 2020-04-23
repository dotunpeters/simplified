import unittest
from simplified import helpers
from simplified import *
import random

with app.app_context():
    render = Products.query.paginate(page=random.randint(2, 10), per_page=random.randint(2, 10))

class Test_more_route(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.assertEqual(app.debug, False)


    # executed after each test
    def tearDown(self):
        pass

    def test_parser(self):
        products = helpers.parser(render)
        self.assertTrue(products)
        self.assertEqual(products[0]['success'], True)
        self.assertGreater(len(products[1]), 1)
        self.assertIn("name", products[1])
        self.assertIn("sku", products[1])
        self.assertIn("price", products[1])
        self.assertIn("stars", products[1])
        self.assertIn("original", products[1])

        self.assertIn("link", products[1])
        self.assertIsInstance(products[1]["link"], str)

        self.assertIn("image_url", products[1])
        self.assertIsInstance(products[1]["image_url"], str)

        self.assertIn("reviews", products[1])
        self.assertIn("seller", products[1])
        self.assertIn("category", products[1])
        self.assertIn("description", products[1])

if __name__ == '__main__':
    unittest.main()
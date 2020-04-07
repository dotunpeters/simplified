import unittest
import application
from application import app
import requests
import os

class Test_more_route(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def test_more(self):
        data = {"page": 2}
        requests.get("http://127.0.0.1:5000/")
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], True)

if __name__ == '__main__':
    unittest.main()

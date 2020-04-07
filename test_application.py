import unittest
import application
from application import app
import requests
import random
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
        categories = ["home", "computing", "electronics", "health-and-beauty", "fashion", "home-and-office", "phones-and-tablets"]

        #first more api route test
        data = {"page": random.randint(2, 20), "test": random.choice(categories)}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], True)

        #second more api route test
        data = {"page": random.randint(2, 20), "test": random.choice(categories)}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], True)

        #third more api route test
        data = {"page": random.randint(2, 20), "test": random.choice(categories)}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], True)

        #fourth more api route test
        data = {"page": random.randint(2, 20), "test": " "}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], False)

        #fifth more api route test
        data = {"page": 0, "test": random.choice(categories)}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], False)

        queries = ["tv", "samsung", "watch", "notebook", "cloth", "phone", "washing machine"]
        #Search query more api route test
        data = {"page": 2, "test": "search", "query": random.choice(queries)}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], True)

        #Category Search query more api route test
        data = {"page": 2, "test": "cat-search", "query": f"20,{random.choice(categories)}"}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], True)

if __name__ == '__main__':
    unittest.main()

from flask import url_for
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

        #Category computing Search query more api route test
        query = ["laptop", "charger", "notebook", "intel", "macbook"]
        data = {"page": 2, "test": "cat-search", "query": f"{random.choice(query)},computing"}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], True)

        #Category electronics Search query more api route test
        query = ["tv", "camera", "bluetooth", "television", "speaker"]
        data = {"page": 2, "test": "cat-search", "query": f"{random.choice(query)},electronics"}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], True)

        #Category fashion Search query more api route test
        query = ["shoe", "bag", "necklace", "shirt"]
        data = {"page": 2, "test": "cat-search", "query": f"{random.choice(query)},fashion"}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], True)

        #Category health-and-beauty Search query more api route test
        query = ["clipper", "soap", "brush", "powder"]
        data = {"page": 2, "test": "cat-search", "query": f"{random.choice(query)},health and beauty"}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], True)

        #Category home-and-office Search query more api route test
        query = ["fan", "oven", "freezer"]
        data = {"page": 2, "test": "cat-search", "query": f"{random.choice(query)},home and office"}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], True)

        #Category phones-and-tablets Search query more api route test
        query = ["android", "iphone", "tecno", "infinix", "samsung"]
        data = {"page": 2, "test": "cat-search", "query": f"{random.choice(query)},phones and tablets"}
        result = requests.post("http://127.0.0.1:5000/more", data=data).json()
        self.assertEqual(result[0]["success"], True)

    def test_home(self):
        #home route test
        result = requests.get("http://127.0.0.1:5000")
        self.assertEqual(result.status_code, 200)

        result = requests.get("http://127.0.0.1:5000/feeds")
        self.assertEqual(result.status_code, 200)

    def test_category(self):
        #category route test
        categories = ["home", "computing", "electronics", "health-and-beauty", "fashion", "home-and-office", "phones-and-tablets"]
        result = requests.get(f"http://127.0.0.1:5000/category/{random.choice(categories)}")
        self.assertEqual(result.status_code, 200)

    def test_search(self):
        #category route test
        query = ["android", "iphone", "tecno", "infinix", "samsung"]
        categories = ["home", "computing", "electronics", "health-and-beauty", "fashion", "home-and-office", "phones-and-tablets"]
        result = requests.get(f"http://127.0.0.1:5000/search/{random.choice(categories)}/20")
        self.assertEqual(result.status_code, 200)

        result = requests.get(f"http://127.0.0.1:5000/search/{random.choice(categories)}/20")
        self.assertEqual(result.status_code, 200)

    def test_search_query(self):
        #category route test
        query = ["android", "iphone", "tecno", "infinix", "samsung"]
        data = {"query": random.choice(query)}
        result = requests.get(f"http://127.0.0.1:5000/search", params=data)
        self.assertEqual(result.status_code, 200)

        data = {"query": random.choice(query)}
        result = requests.get(f"http://127.0.0.1:5000/search", params=data)
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()

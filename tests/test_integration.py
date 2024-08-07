import unittest

import requests


class TestIntegration(unittest.TestCase):
    def test_index(self):
        response = requests.request(
            "GET",
            "http://localhost/",
        )
        self.assertEqual(response.status_code, 200)
        try:
            response = requests.request(
                "POST",
                "http://localhost/",
            )
        except Exception as e:
            print(e)
            
            
        self.assertEqual(response.status_code, 200)

    def test_predict(self):
        files = [("file", ("dog.jpeg", open("tests/dog.jpeg", "rb"), "image/jpeg"))]
        headers = {}
        payload = {}
        try:
            response = requests.request(
                "POST",
                "http://0.0.0.0/predict",
                headers=headers,
                data=payload,
                files=files,
            )
        except Exception as e:
              print(e)
              
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data.keys()), 3)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["prediction"], "Eskimo_dog")
        self.assertAlmostEqual(data["score"], 0.9346, 5)


if __name__ == "__main__":
    unittest.main()

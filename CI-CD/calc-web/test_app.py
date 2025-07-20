import unittest
import app

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def test_add(self):
        response = self.client.get("/add?a=5&b=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["result"], 7)

    def test_subtract(self):
        response = self.client.get("/subtract?a=5&b=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["result"], 3)

if __name__ == '__main__':
    unittest.main()

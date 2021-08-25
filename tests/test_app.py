import unittest

from flaskr import create_app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app("development").test_client()

    def test_app(self):
        response = self.app.get("/test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["msg"], "ok")


if __name__ == "__main__":
    unittest.main()

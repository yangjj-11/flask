import unittest

from manage import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_app(self):
        response = self.app.get("/test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["msg"], "ok")


if __name__ == "__main__":
    unittest.main()

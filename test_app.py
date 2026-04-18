---

### File 2: `test_app.py`
Unit tests prove to the judges that your code is reliable. Create a file named `test_app.py` and paste this code. It uses Python's built-in testing library to verify that your API correctly blocks invalid requests.

```python
import unittest
from app import app

class GrabpicTestCase(unittest.TestCase):
    def setUp(self):
        # Creates a test client to ping our API without turning on the actual server
        self.client = app.test_client()

    def test_authenticate_no_file(self):
        # Test what happens if someone sends a request with no selfie attached
        response = self.client.post('/authenticate')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"No image uploaded", response.data)

    def test_get_images_invalid_id(self):
        # Test what happens if we search for a grab_id that doesn't exist
        response = self.client.get('/images/999999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"No images found", response.data)

if __name__ == '__main__':
    unittest.main()

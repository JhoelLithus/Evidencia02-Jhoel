import base64
from server import app
import unittest

class MyTestCase(unittest.TestCase):
    def setUp(self):    
        self.app = app.test_client()
    
    def tearDown(self):
        pass

    def open_with_auth(self, url, method, username, password):
        return self.app.open(url,
            method=method,
            headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')
            }
        )
    
    def test_login(self):
        res = self.open_with_auth('/login', 'GET', 'jhoel', 'jhoel')

if __name__ == '__main__':

     unittest.main()

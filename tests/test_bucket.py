from api.bucket import app
from flask import json
from instance.config import application_config
import unittest


class TestBucket(unittest.TestCase):
    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()

        self.user = json.dumps({
            'name': 'emma',
            'email': '1234@gmail.com',
            'password': '12345678'
        })
        response = self.client.post('/auth/register', data=self.user)
        json_data = json.loads(response.data.decode())
        self.token = json_data['token']

    def test_add_bucket_without_name(self):
        bucket = json.dumps({
            'name': '',
            'desc': 'rally wins'
        })
        response = self.client.post('/buckets', data=bucket})
        self.assertEquals(response.status_code, 400)
        self.assertIn('Missing details', response.data.decode())



    # def test_add_bucket_successfully(self):
    #     new_bucket = json.dumps({
    #         'name': 'Adventure',
    #         'desc': 'Rallying'
    #     })
    #     response = self.client.post('/buckets', data=new_bucket,
    #                                 headers={"Authorization": self.token})
    #     self.assertEquals(response.status_code, 201)
    #     self.assertIn('Bucket', response.data.decode())
    #     self.tearDown()

    def tearDown(self):
        self.user =None
        self.token = None
        self.client = None


    if __name__ == '__main__':
        unittest.main()

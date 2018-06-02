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
        self.bucket = json.dumps({
            'name': 'Adventure',
            'desc': 'Touring'
        })
        self.bucket_conf = json.dumps({
            'name': 'Rally',
            'desc': 'Rally'
        })
        response = self.client.post('/auth/register', data=self.user)

    def test_add_bucket_without_name(self):
        bucket = json.dumps({
            'name': '',
            'desc': 'rally wins'
        })
        response = self.client.post('/buckets', data=bucket)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Missing details', response.data.decode())

    def test_add_bucket_successfully(self):
        bucket = json.dumps({
            'name': 'Adventure',
            'desc': 'Rallying'
        })
        response = self.client.post('/buckets', data=bucket)
        self.assertEquals(response.status_code, 201)
        self.assertIn('Bucket', response.data.decode())

    def test_add_bucket_with_existing_bucket(self):

        self.client.post('/buckets', data=self.bucket_conf)
        response = self.client.post('/buckets', data=self.bucket_conf)
        self.assertEquals(response.status_code, 409)
        self.assertIn('Bucket already exists', response.data.decode())


    def test_get_all_buckets_on_empty_bucket_list(self):
        self.tearDown()
        response = self.client.get('/buckets')
        self.assertEquals(response.status_code, 404)
        self.assertIn('No buckets available', response.data.decode())



    if __name__ == '__main__':
        unittest.main()

from api.bucket import app
from flask import json
from instance.config import application_config
import unittest


class TestBucket(unittest.TestCase):
    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()


        self.bucket = json.dumps({
            'name': 'Adventure',
            'desc': 'Rallying'
        })

        self.bucket2 = json.dumps({
            'name': 'Food',
            'desc': 'Priscilla'
        })

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
        response = self.client.post('/buckets', data=self.bucket)
        self.assertEquals(response.status_code, 201)
        self.assertIn('Bucket', response.data.decode())


    def test_add_bucket_with_existing_bucket(self):

        self.client.post('/buckets', data=self.bucket_conf)
        response = self.client.post('/buckets', data=self.bucket_conf)
        self.assertEquals(response.status_code, 409)
        self.assertIn('Bucket already exists', response.data.decode())
        self.tearDown()


    # def test_get_all_buckets_on_empty_bucket_list(self):
    #     response = self.client.get('/buckets')
    #     self.assertEquals(response.status_code, 404)
    #     self.assertIn('No buckets available', response.data.decode())

    def test_get_single_bucket_with_no_id(self):
        self.tearDown()
        response = self.client.get('/buckets/0')
        self.assertEquals(response.status_code, 400)
        self.assertIn('Bucket id missing', response.data.decode())
        self.tearDown()

    # def test_get_single_bucket_with_no_bucket_list(self):
    #     self.tearDown()
    #     response = self.client.get('/buckets/1')
    #     self.assertEquals(response.status_code, 400)
    #     self.assertIn('No bucket list added', response.data.decode())


    def test_get_single_bucket_that_does_not_exist(self):
        self.tearDown()
        self.client.post('/buckets', data=self.bucket2)
        response = self.client.get('/buckets/45')
        self.assertEquals(response.status_code, 404)
        self.assertIn('Bucket does not exist', response.data.decode())
        self.tearDown()

    def test_get_single_bucket_successfully(self):
        self.tearDown()
        self.client.post('/buckets', data=self.bucket2)
        response = self.client.get('/buckets/1')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Bucket', response.data.decode())
        self.tearDown()

    def tearDown(self):
       from models.bucket_model import bucket
       self.buck = bucket
       self.buck =[]
       bucket = self.buck






    if __name__ == '__main__':
        unittest.main()

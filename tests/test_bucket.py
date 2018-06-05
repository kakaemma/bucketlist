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

    def test_get_all_buckets_on_empty_bucket_list(self):
        """ Test get all buckets when bucket list is empty"""
        response = self.client.get('/buckets')
        self.assertEquals(response.status_code, 404)
        self.assertIn('No buckets available', response.data.decode())

    def test_get_single_bucket_with_no_id(self):
        """Return bucket Id missing"""
        self.tearDown()
        response = self.client.get('/buckets/0')
        self.assertEquals(response.status_code, 400)
        self.assertIn('Bucket id missing', response.data.decode())
        self.tearDown()

    def test_get_single_bucket_with_no_bucket_list(self):
        """ Should return no bucket list added"""
        self.tearDown()
        response = self.client.get('/buckets/1')
        self.assertEquals(response.status_code, 400)
        self.assertIn('No bucket list added', response.data.decode())


    def test_get_single_bucket_that_does_not_exist(self):
        """ Should return bucket does not exist"""
        self.client.post('/buckets', data=self.bucket2)
        response = self.client.get('/buckets/45')
        self.assertEquals(response.status_code, 404)
        self.assertIn('Bucket does not exist', response.data.decode())

    def test_get_single_bucket_successfully(self):
        """ Return message with bucket"""
        self.client.post('/buckets', data=self.bucket2)
        response = self.client.get('/buckets/1')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Bucket', response.data.decode())

    def test_add_bucket_without_name(self):
        """ Should return missing details"""
        bucket = json.dumps({
            'name': '',
            'desc': 'rally wins'
        })
        response = self.client.post('/buckets', data=bucket)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Missing details', response.data.decode())

    def test_add_bucket_successfully(self):
        """Return message with bucket on success"""
        response = self.client.post('/buckets', data=self.bucket)
        self.assertEquals(response.status_code, 201)
        self.assertIn('Bucket', response.data.decode())


    def test_add_bucket_with_existing_bucket(self):
        """Return bucket already exists"""
        self.client.post('/buckets', data=self.bucket_conf)
        response = self.client.post('/buckets', data=self.bucket_conf)
        self.assertEquals(response.status_code, 409)
        self.assertIn('Bucket already exists', response.data.decode())
        self.tearDown()




    def tearDown(self):
        from models.bucket_model import BucketModal
        BucketModal.bucket =[]

    if __name__ == '__main__':
        unittest.main()

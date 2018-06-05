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
        self.bucket_mod = json.dumps({
            'name': '',
            'desc': ''
        })
        self.bucket_mod_final = json.dumps({
            'name': 'FootBall',
            'desc': 'Winners'
        })
        # response = self.client.post('/auth/register', data=self.user)

    def test_get_all_buckets_on_empty_bucket_list(self):
        """ Test get all buckets when bucket list is empty"""
        response = self.client.get('/buckets')
        self.assertEquals(response.status_code, 404)
        self.assertIn('No buckets available', response.data.decode())

    def test_get_single_bucket_with_no_id(self):
        """Return bucket Id missing"""
        response = self.client.get('/buckets/0')
        self.assertEquals(response.status_code, 400)
        self.assertIn('Bucket id missing', response.data.decode())

    def test_get_single_bucket_with_no_bucket_list(self):
        """ Should return no bucket list added"""
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

    def test_modify_bucket_with_missing_details(self):
        """ Should return missing details and status code 400"""
        self.client.post('/buckets', data=self.bucket)
        response = self.client.put('buckets/1', data=self.bucket_mod)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Missing details', response.data.decode())

    def test_modify_bucket_on_empty_bucket_list(self):
        """
        Should return no buckets available on modifying 
        with empty bucket list
        """
        response = self.client.put('buckets/1', data=self.bucket)
        self.assertEquals(response.status_code, 400)
        self.assertIn('No buckets available', response.data.decode())

    def test_modify_bucket_with_same_bucket_name(self):
        """ Should return cannot modify bucket with the same name"""
        self.client.post('/buckets', data=self.bucket)
        response = self.client.put('/buckets/1', data=self.bucket)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Bucket name can not be the same',
                      response.data.decode())

    def test_modify_bucket_successfully(self):
        """ Should return successfully modified bucket"""
        self.client.post('/buckets', data=self.bucket)
        response = self.client.put('/buckets/1', data=self.bucket_mod_final)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Bucket successfully modified',
                      response.data.decode())

    def tearDown(self):
        from models.bucket_model import BucketModal
        BucketModal.bucket =[]

    if __name__ == '__main__':
        unittest.main()

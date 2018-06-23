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
            'email': 'ek@gmail.com',
            'password': '12345678'
        })
        self.user_login = json.dumps({
            'email': 'ek@gmail.com',
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
        response = self.client.post('/auth/register',
                                    content_type='application/json',
                                    data=self.user)
        res = self.client.post('/auth/login',
                               content_type='application/json',
                               data=self.user_login)
        json_repr = json.loads(res.data.decode())
        self.token = json_repr['token']
        self.header = {'Authorization': self.token}


    def test_get_all_buckets_on_empty_bucket_list(self):
        """ Test get all buckets when bucket list is empty"""
        response = self.client.get('/buckets', headers=self.header)
        self.assertEquals(response.status_code, 404)
        self.assertIn('No buckets available', response.data.decode())

    def test_get_single_bucket_with_no_id(self):
        """Return bucket Id missing"""
        response = self.client.get('/buckets/0', headers=self.header)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Bucket id missing', response.data.decode())

    def test_get_single_bucket_with_no_bucket_list(self):
        """ Should return no bucket list added"""
        response = self.client.get('/buckets/1', headers=self.header)
        self.assertEquals(response.status_code, 400)
        self.assertIn('No bucket list added', response.data.decode())

    def test_get_single_bucket_that_does_not_exist(self):
        """ Should return bucket does not exist"""
        self.client.post('/buckets', content_type='application/json',
                         data=self.bucket2,
                         headers=self.header)
        response = self.client.get('/buckets/45', headers=self.header)
        self.assertEquals(response.status_code, 404)
        self.assertIn('Bucket does not exist', response.data.decode())

    def test_get_single_bucket_successfully(self):
        """ Return message with bucket"""
        self.client.post('/buckets', content_type='application/json',
                         data=self.bucket2, headers=self.header)
        response = self.client.get('/buckets/1', headers=self.header)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Bucket', response.data.decode())

    def test_add_bucket_without_name(self):
        """ Should return missing details"""
        bucket = json.dumps({
            'name': '',
            'desc': 'rally wins'
        })
        response = self.client.post('/buckets',
                                    content_type='application/json',
                                    data=bucket, headers=self.header)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Missing details', response.data.decode())

    def test_add_bucket_successfully(self):
        """Return message with bucket on success"""
        response = self.client.post('/buckets',
                                    content_type='application/json',
                                    data=self.bucket, headers=self.header)
        self.assertEquals(response.status_code, 201)
        self.assertIn('Bucket', response.data.decode())

    def test_add_bucket_with_existing_bucket(self):
        """Return bucket already exists"""
        self.client.post('/buckets',
                         content_type='application/json',
                         data=self.bucket_conf, headers=self.header)
        response = self.client.post('/buckets',
                                    content_type='application/json',
                                    data=self.bucket_conf,
                                    headers=self.header)
        self.assertEquals(response.status_code, 409)
        self.assertIn('Bucket already exists', response.data.decode())

    def test_modify_bucket_with_missing_details(self):
        """ Should return missing details and status code 400"""
        self.client.post('/buckets',
                         content_type='application/json', data=self.bucket)
        response = self.client.put('buckets/1',
                                    content_type='application/json',
                                   data=self.bucket_mod,
                                   headers=self.header)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Missing details', response.data.decode())

    def test_modify_bucket_on_empty_bucket_list(self):
        """
        Should return no buckets available on modifying
        with empty bucket list
        """
        response = self.client.put('buckets/1',
                                   content_type='application/json',
                                   data=self.bucket,
                                   headers=self.header)
        self.assertEquals(response.status_code, 400)
        self.assertIn('No buckets available', response.data.decode())

    def test_modify_bucket_with_same_bucket_name(self):
        """ Should return cannot modify bucket with the same name"""
        self.client.post('/buckets',
                         content_type='application/json',
                         data=self.bucket,
                         headers=self.header)
        response = self.client.put('/buckets/1',
                                   content_type='application/json',
                                   data=self.bucket,
                                   headers=self.header)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Bucket name can not be the same',
                      response.data.decode())

    def test_modify_bucket_successfully(self):
        """ Should return successfully modified bucket"""
        self.client.post('/buckets',
                         content_type='application/json',
                         data=self.bucket,headers=self.header)
        response = self.client.put('/buckets/1',
                                    content_type='application/json',
                                   data=self.bucket_mod_final,
                                   headers=self.header)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Bucket successfully modified',
                      response.data.decode())

    def test_delete_bucket_on_empty_bucket_list(self):
        """ Should return can not delete on empty bucket list"""
        response = self.client.delete('buckets/1', headers=self.header)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Can not delete on empty Bucket list',
                      response.data.decode())

    def test_delete_bucket_successfully(self):
        """ Should return bucket successfully deleted"""
        self.client.post('/buckets',
                                    content_type='application/json',
                         data=self.bucket,
                         headers=self.header)
        response = self.client.delete('buckets/1', headers=self.header)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Bucket successfully deleted',
                      response.data.decode())



    def tearDown(self):
        from models.bucket_model import BucketModal
        BucketModal.bucket =[]

    if __name__ == '__main__':
        unittest.main()

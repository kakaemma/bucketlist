from api.bucket import app
from flask import jsonify,json
from instance.config import application_config
import unittest

class TestItem(unittest.TestCase):

    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()
        self.item = json.dumps({
            'name': 'music',
            'status': 'pending'
        })
        self.item_edit = json.dumps({
            'name': 'music playing',
            'status': 'done'
        })
        self.item_empty = json.dumps({
            'name': '',
            'status': ''
        })
        self.bucket = json.dumps({
            'name': 'Adventure',
            'desc': 'Rallying'
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
        res = self.client.post('/auth/login',
                               content_type='application/json',
                               data=self.user_login)
        json_repr = json.loads(res.data.decode())
        self.token = json_repr['token']
        self.header = {'Authorization': self.token}

    def test_add_item_with_missing_details(self):
        response = self.client.post('/buckets/1/items',
                                    content_type='application/json',
                                    data=self.item_empty)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Missing Details', response.data.decode())

    def test_add_item_with_no_bucket_list(self):
        response = self.client.post('/buckets/1/items',
                                    content_type='application/json',
                                    data=self.item)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Attempting to add item on empty bucket list',
                      response.data.decode())

    def test_add_item_on_non_existing_bucket(self):
        self.client.post('/buckets',
                                    content_type='application/json',
                         data=self.bucket, headers=self.header)
        response = self.client.post('/buckets/4/items',
                                    content_type='application/json',
                                    data=self.item)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Adding Bucket item to non existing bucket',
                      response.data.decode())

    def test_add_item_successfully(self):
        self.client.post('/buckets',
                                    content_type='application/json',
                         data=self.bucket, headers=self.header)
        response = self.client.post('/buckets/1/items',
                                    content_type='application/json',
                                    data=self.item)
        self.assertEquals(response.status_code, 201)
        self.assertIn('Bucket item successfully added',
                      response.data.decode())

    def test_modify_item_with_empty_values(self):
        self.client.post('/buckets',
                                    content_type='application/json',
                         data=self.bucket, headers=self.header)
        response = self.client.put('/buckets/1/items/1',
                                    content_type='application/json',
                                    data=self.item_empty)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Missing details',
                      response.data.decode())

    def test_modify_item_on_empty_bucket(self):
        response = self.client.put('/buckets/1/items/1',
                                    content_type='application/json',
                                    data=self.item_edit)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Can not edit item on empty bucket list',
                      response.data.decode())

    def test_modify_item_on_non_existing_bucket(self):
        self.client.post('/buckets',
                                    content_type='application/json',
                         data=self.bucket, headers=self.header)
        self.client.post('/buckets/1/items',
                                    content_type='application/json',
                                    data=self.item)
        response = self.client.put('/buckets/2/items/1',
                                    content_type='application/json',
                                   data=self.item_edit)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Attempting to modify item on non existing bucket',
                      response.data.decode())

    def test_modify_item_on_non_existing_item(self):
        self.client.post('/buckets',
                                    content_type='application/json',
                         data=self.bucket, headers=self.header)
        self.client.post('/buckets/1/items',
                                    content_type='application/json',
                                    data=self.item)
        response = self.client.put('/buckets/1/items/3',
                                    content_type='application/json',
                                   data=self.item_edit)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Attempting to modify item on non existing item',
                      response.data.decode())

    def test_modify_item_successfully(self):
        """ Should return item successfully updated"""
        self.client.post('/buckets',
                                    content_type='application/json',
                         data=self.bucket, headers=self.header)
        self.client.post('/buckets/1/items',
                                    content_type='application/json',
                                    data=self.item)
        response = self.client.put('/buckets/1/items/1',
                                    content_type='application/json',
                                   data=self.item_edit)
        self.assertEquals(response.status_code, 200)
        self.assertIn('Item successfully updated',
                      response.data.decode())

    def test_delete_item_with_no_bucket_list(self):
        response = self.client.delete('/buckets/1/items/1')
        self.assertEquals(response.status_code, 400)
        self.assertIn('Can not delete item on empty bucket list',
                      response.data.decode())

    def test_delete_item_with_wrong_id(self):
        self.client.post('/buckets',
                                    content_type='application/json',
                         data=self.bucket, headers=self.header)
        self.client.post('/buckets/1/items',
                                    content_type='application/json',
                                    data=self.item)
        response = self.client.delete('/buckets/1/items/2')
        self.assertEquals(response.status_code, 400)
        self.assertIn('Attempting to delete non existing item',
                      response.data.decode())

    def test_delete_item_with_non_existing_bucket(self):
        """ Should return error on non existing bucket"""
        self.client.post('/buckets',
                                    content_type='application/json',
                         data=self.bucket, headers=self.header)
        self.client.post('/buckets/1/items',
                                    content_type='application/json',
                                    data=self.item)
        response = self.client.delete('/buckets/2/items/1')
        self.assertEquals(response.status_code, 400)
        self.assertIn('Attempting to delete item on non existing bucket',
                      response.data.decode())

    def test_delete_item_successfully(self):
        """ Should return item successfully deleted"""
        self.client.post('/buckets',
                                    content_type='application/json',
                         data=self.bucket, headers=self.header)
        self.client.post('/buckets/1/items',
                                    content_type='application/json',
                                    data=self.item)
        response = self.client.delete('/buckets/1/items/1')
        self.assertEquals(response.status_code, 200)
        self.assertIn('Item successfully deleted', response.data.decode())







    def tearDown(self):
        from models.bucket_model import BucketModal
        from models.item_model import BucketItems
        BucketModal.bucket =[]
        BucketItems.items = []


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
        self.item_empty = json.dumps({
            'name': '',
            'status': ''
        })
        self.bucket = json.dumps({
            'name': 'Adventure',
            'desc': 'Rallying'
        })

    def test_add_item_with_missing_details(self):
        response = self.client.post('/buckets/1/items',
                                    data=self.item_empty)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Missing Details', response.data.decode())

    def test_add_item_with_no_bucket_list(self):
        response = self.client.post('/buckets/1/items', data=self.item)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Attempting to add item on empty bucket list',
                      response.data.decode())

    def test_add_item_on_non_existing_bucket(self):
        self.client.post('/buckets', data=self.bucket)
        response = self.client.post('/buckets/4/items',
                                    data=self.item)
        self.assertEquals(response.status_code, 400)
        self.assertIn('Adding Bucket item to non existing bucket',
                      response.data.decode())

    def test_add_item_successfully(self):
        self.client.post('/buckets', data=self.bucket)
        response = self.client.post('/buckets/1/items',
                                    data=self.item)
        self.assertEquals(response.status_code, 201)
        self.assertIn('Bucket item successfully added',
                      response.data.decode())


    def tearDown(self):
        from models.bucket_model import BucketModal
        from models.item_model import BucketItems
        BucketModal.bucket =[]
        BucketItems.items = []


from flask import jsonify
from models.bucket_model import BucketModal
from models.item_model import BucketItems

class Item(object):
    """
    This class adds perform Item operations on the bucket list
    """


    @classmethod
    def add_item(cls,  item_name, status, bucket_id, user_id=1,):
        """
        This controls adding an item to the bucket list
        :param user_id: 
        :param item_name: 
        :param status: 
        :param bucket_id: 
        :return: 
        """
        if not item_name or not status or not bucket_id or not user_id:
            response = jsonify({'Error': 'Missing Details'})
            response.status_code = 400
            return response

        check_for_bucket_list = BucketModal.check_for_buckets_available()
        if not check_for_bucket_list:
            response = jsonify({
                'Error': 'Attempting to add item on empty bucket list'
            })
            response.status_code = 400
            return response

        check_if_bucket_exist = BucketModal.check_bucket_with_id(bucket_id)

        if not check_if_bucket_exist:
            response = jsonify(
                {'Error': 'Adding Bucket item to non existing bucket'
                 })
            response.status_code = 400
            return response

        if check_if_bucket_exist:
            new_item = BucketItems(user_id,bucket_id,item_name,status)
            new_item.add_item()
            response = jsonify({'status': 'Bucket item successfully added'})
            response.status_code = 201
            return response


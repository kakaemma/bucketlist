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
    #-----------------------------------------------------------------------

    @classmethod
    def edit_item(cls, bucket_id, new_name, new_status, item_id, user_id=1):
        """
        This controls modifying an item
        :param bucket_id: 
        :param new_name: 
        :param new_status: 
        :param item_id: 
        :param user_id: 
        :return: 
        """

        if not bucket_id or not new_name or not new_status \
                or not item_id or not user_id:
            response = jsonify({'Error': 'Missing details'})
            response.status_code = 400
            return response

        bucket = BucketModal.check_for_buckets_available()

        if not bucket:
            response = jsonify({
                'Error': 'Can not edit item on empty bucket list'
            })
            response.status_code = 400
            return response

        bucket_exist = BucketModal.check_bucket_with_id(bucket_id)

        if not bucket_exist:
            response = jsonify(
                {'Error': 'Attempting to modify item on non existing bucket'
                 })
            response.status_code = 400
            return response

        item = BucketItems.check_item_with_id(item_id)
        if not item:
            response = jsonify(
                {'Error': 'Attempting to modify item on non existing item'
                 })
            response.status_code = 400
            return response

        edit_item = BucketItems.update_item(bucket_id,
                                            item_id, new_name, new_status)
        if edit_item:
            response = jsonify(
                {'Error': 'Item successfully updated'
                 })
            response.status_code = 200
            return response
    #-----------------------------------------------------------------------
    @classmethod
    def delete_item(cls,bucket_id, item_id):
        """
        Controller for deleting item
        :param item_id: 
        :return: 
        """
        if not item_id or not bucket_id:
            response = jsonify(
                {'Error': 'Item Id missing'
                 })
            response.status_code = 400
            return response

        item_bucket = BucketModal.check_for_buckets_available()

        if not item_bucket:
            response = jsonify({
                'Error': 'Can not delete item on empty bucket list'
            })
            response.status_code = 400
            return response

        bucket_in_sys = BucketModal.check_bucket_with_id(bucket_id)

        if not bucket_in_sys:
            response = jsonify(
                {'Error': 'Attempting to delete item on non existing bucket'
                 })
            response.status_code = 400
            return response

        item = BucketItems.check_item_with_id(item_id)
        if not item:
            response = jsonify(
                {'Error': 'Attempting to delete non existing item'
                 })
            response.status_code = 400
            return response

        delete_item = BucketItems.delete_item(bucket_id, item_id)
        response = jsonify({
            'status': 'Item successfully deleted'
        })
        response.status_code = 200
        return response






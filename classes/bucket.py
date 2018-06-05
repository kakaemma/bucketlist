from flask import jsonify
from models.bucket_model import BucketModal


class Bucket(object):

    @classmethod
    def add_bucket(cls, name, desc):
        """
        This validates and controls adding bucket 
        :param name: 
        :param desc: 
        :return: 
        """
        if not name or not desc:
            response = jsonify({'Error': 'Missing details'})
            response.status_code = 400
            return response

        check_bucket = BucketModal.get_bucket_by_name(name)
        if check_bucket:
            response = jsonify({
                'Conflict': 'Bucket already exists'
            })
            response.status_code = 409
            return response

        if not check_bucket:
            bucket = BucketModal(name, desc)
            bucket.create_bucket()

            response = jsonify({
                    'message': 'Bucket ' + name + ' added',
                    'id': 'user_id'
            })
            response.status_code = 201
            return response

    #---------------------------------------------------------------------

    @staticmethod
    def modify_bucket(edit_id, name, desc):
        """
        This method validates and controls editing an existing bucket
        :param edit_id: 
        :param name: 
        :param desc: 
        :return: 
        """
        if not name or not edit_id or not desc:
            response = jsonify({'Error': 'Missing details'})
            response.status_code = 400
            return response

        bucket_available = BucketModal.check_for_buckets_available()
        if not bucket_available:
            response = jsonify({'status': 'No buckets available'})
            response.status_code = 400
            return response

        edit_this_bucket = BucketModal.modify_bucket(edit_id, name, desc)

        if edit_this_bucket:
            response = jsonify({'status': 'Bucket successfully modified'})
            response.status_code = 200
            return response

        response = jsonify({'Error': 'Bucket name can not be the same'})
        response.status_code = 400
        return response
    #---------------------------------------------------------------------

    @staticmethod
    def get_all_buckets():
        """
        This controls getting all buckets available in the system
        :return: 
        """
        bucket_available = BucketModal.check_for_buckets_available()
        if  bucket_available :
            buckets = BucketModal.get_buckets()
            response = jsonify({'Bucket List': buckets})
            response.status_code = 200
            print(bucket_available)
            return response

        response = jsonify({'status': 'No buckets available'})
        response.status_code = 404
        return response




     #---------------------------------------------------------------------

    @staticmethod
    def get_single_bucket(bucket_id):
        """
        This method controls getting a single bucket from the system
        :param bucket_id: 
        :return: 
        """
        if not bucket_id:
            response = jsonify({'status': 'Bucket id missing'})
            response.status_code = 400
            return response

        check_for_buckets = BucketModal.check_for_buckets_available()
        print(check_for_buckets)
        if check_for_buckets:
            single_bucket = BucketModal.get_bucket(bucket_id)
            if not single_bucket:
                response = jsonify({'status': 'Bucket does not exist'})
                response.status_code = 404
                return response

            response = jsonify({
                'status': 'Bucket retrieved',
                'Bucket': single_bucket
            })
            response.status_code = 200
            return response

        response = jsonify({'status': 'No bucket list added'})
        response.status_code = 400
        return response





    #---------------------------------------------------------------------

    @staticmethod
    def delete_bucket_from_bucket_list(bucket_id):
        """
        This method controls deleting a single bucket from the system
        :param bucket_id: 
        :return: 
        """
        if not bucket_id:
            response = jsonify({'status': 'bucket id missing'})
            response.status_code = 400
            return response

        bucket_list = BucketModal.check_for_buckets_available()
        if bucket_list == 0:
            response = jsonify({
                'status': 'Can not delete on empty Bucket list'
            })
            response.status_code = 400
            return response

        delete_this = BucketModal.delete_bucket(bucket_id)
        if delete_this:
            response = jsonify({'status': 'Bucket successfully deleted'})
            response.status_code = 200
            return response

        response = jsonify({
            'status': 'Bucket with id ' + bucket_id +' does not exist'
        })
        response.status_code = 404
        return response
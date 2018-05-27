from flask import jsonify
from models.bucket_model import BucketModal

class Bucket(object):

    @classmethod
    def add_bucket(cls, name, desc, user_id):
        if not name or not desc:
            response = jsonify({'Error': 'Missing details'})
            response.status_code = 400
            return response


        add_bucket = BucketModal(name, desc)
        response = jsonify({
            'message': 'Bucket " ' + name + ' " added',
            'id': user_id
        })
        response.status_code = 201
        return response

from flask import jsonify
from validate_email import validate_email
from models.users import UserModal,users


class Authenticate(object):

    """ 
    This takes care of all user operations 
    from registration to login
    """

    @staticmethod
    def register(name, email, password):
        if not name or not email or not password:
            response = jsonify({'Error': 'Missing value(s)'})
            response.status_code = 406
            return response

        if not len(name) >= 3:
            response = jsonify({'Error': 'name too short'})
            response.status_code = 422
            return response

        if not len(password) > 6:
            response = jsonify({'Error': 'Password too short'})
            response.status_code = 422
            return response

        if not validate_email(email):
            response = jsonify({'Error': 'Invalid Email address'})
            response.status_code = 422
            return response

        check_user = UserModal.check_user_email(email)
        if email != check_user:
            new_user = UserModal(name, email, password)
            new_user.add_user()
            response = jsonify({'message': 'User successfully registered'})
            response.status_code = 201
            return response

        response = jsonify({'Conflict': 'Email already exists'})
        response.status_code = 409
        return response



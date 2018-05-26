users = []

class UserModal(object):

    def __init__(self, name, email, password):
        self.id = len(users)+1
        self.name = name
        self.email = email
        self.password = password

    def add_user(self):
        users.append(self)



    @staticmethod
    def check_user_email(email):
        for user in users:
            if user.email == email:
                return user.email
            return 'no user'

    @classmethod
    def get_user_id(cls, email):
        for user in users:
            if user.email == email:
                return user.id

    @classmethod
    def get_user_by_id(cls, user_id):
        for user in users:
            if user.id == user_id:
                return user.id

    @staticmethod
    def check_user(email, password):
        for user in users:
            if user.email == email and user.password == password:
                response = user.id
                return response


    @staticmethod
    def check_user_email(email):
        for user in users:
            if user.email == email:
                response = user.email
                return response

    @staticmethod
    def check_user_return_pass(email):
        for user in users:
            if user.email == email:
                response = user.password
                return response


    @staticmethod
    def reset_user_pass(email, new_password):
        resp = 'no user'
        for user in users:
            if user.email == email:
                user.password = new_password
                response = user.id
                return response
            return resp




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


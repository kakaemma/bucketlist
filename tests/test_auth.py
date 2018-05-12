import unittest
from flask import json
from api.bucket import app
from instance.config import application_config


class TestAuth(unittest.TestCase):
    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()
        self.user = json.dumps({
            'name': 'emmanuel',
            'email': 'kakaemma@gmail.com',
            'password': '1234567'
        })
        self.empty_user = json.dumps({
            'name': '',
            'email': '',
            'password': ''
        })
        self.wrong_email = json.dumps({
            'name': 'emmanuel',
            'email': 'kaka',
            'password': '1234567'
        })
        self.short_pass = json.dumps({
            'name': 'emmanuel',
            'email': 'kakaemma@gmail.com',
            'password': '12345'
        })
        self.conflict_mail = json.dumps({
            'name': 'emmanuel',
            'email': 'kakaemma@gmail.com',
            'password': '12345'
        })
        self.empty_login = json.dumps({
            'email': '',
            'password': ''
        })
        self.valid_login_user = json.dumps({
            'email': 'kakaemma1@gmail.com',
            'password': '1234567'
        })
        self.invalid_user = json.dumps({
            'email': 'wromguser@gmail.com',
            'password': '7654321'
        })
        self.invalid_login_email = json.dumps({
            'email': 'kakaemma',
            'password': '1234567'
        })
        self.empty_reset_password = json.dumps({
            'email': 'kakaemma1@gmail.com',
            'old_password': '',
            'new_password': ''
        })
        self.wrong_reset_password = json.dumps({
            'email': 'kakaemma1@gmail.com',
            'old_password': '2345678',
            'new_password': '1234567'
        })
        self.wrong_reset_details = json.dumps({
            'email': 'emma1@gmail.com',
            'old_password': '1234568',
            'new_password': 'qwertyui'
        })
        self.reset_details = json.dumps({
            'email': 'kakaemma1@gmail.com',
            'old_password': '1234567',
            'new_password': '7654321'
        })

    def test_index_route(self):
        """ Test response for title in the index page"""
        response = self.client.get('/')
        self.assertIn('Welcome to Bucket List API', response.data.decode())

    def test_registration_with_no_values(self):
        """ Test for registration with empty values"""
        response = self.client.post('/auth/register', data=self.empty_user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Missing login details', response.data.decode())

    def test_registration_with_invalid_email(self):
        """ Should throw invalid email address"""
        response = self.client.post('/auth/register', data=self.wrong_email)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid Email', response.data.decode())

    def test_registration_with_short_password(self):
        """ Should return password too short"""
        response = self.client.post('/auth/register', data=self.short_pass)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Password too short', response.data.decode())

    def test_registration_with_existing_email(self):
        """ Should throw Email exists"""
        self.client.post('/auth/register', data=self.user)
        response = self.client.post('/auth/register', data=self.user)
        self.assertEqual(response.status_code, 409)
        self.assertIn('Email already exists', response.data.decode())

    def test_successful_registration(self):
        """ Should return registration successful and 201 status code"""
        response = self.client.post('/auth/register', data=self.user)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully registered', response.data.decode())

    def test_login_without_credentials(self):
        """ Should throw missing credentials"""
        response = self.client.post('/auth/login', data=self.empty_login)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Missing login credentials', response.data.decode())

    def test_login_with_invalid_email(self):
        """ Should throw invalid email address"""
        response = self.client.post('/auth/login', data=self.invalid_login_email)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid login email', response.data.decode())

    def test_login_with_invalid_credentials(self):
        """ Should throw invalid login credentials"""
        response = self.client.post('/auth/login', data=self.invalid_user)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid Login Details', response.data.decode())

    def test_successful_login(self):
        """ Show login successful """
        #First register the user
        self.client.post('/auth/register', data=self.user)

        response = self.client.post('/auth/login', data=self.valid_login_user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', response.data.decode())

    def test_reset_password_with_no_password(self):
        """ Should throw error for non existing email or password"""
        self.client.post('/auth/register', data=self.user)

        response = self.client.post('/auth/reset-password',
                                    data=self.empty_reset_password)
        self.assertEqual(response.status_code, 403)
        self.assertIn('Missing email or password', response.data.decode())

    def test_reset_password_with_non_existing_email(self):
        """ Throw No account with that email"""
        self.client.post('/auth/register', data=self.user)

        response = self.client.post('/auth/reset-password',
                                    data=self.wrong_reset_details)
        self.assertEqual(response.status_code, 403)
        self.assertIn('Email and password do not exist',
                      response.data.decode())

    def test_reset_password_with_wrong_password(self):
        """ Should throw old password is wrong """
        self.client.post('/auth/register', data=self.user)

        response = self.client.post('/auth/reset-password',
                                    data=self.wrong_reset_password)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Old password does not match',
                      response.data.decode())

    def test_reset_password_successfully(self):
        """ Should show password reset successfully"""
        self.client.post('/auth/register', data=self.user)
        response = self.client.post('/auth/reset-password',
                                    data=self.reset_details)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Password reset successfully',
                      response.data.decode())











if __name__ == '__main__':
    unittest.main()
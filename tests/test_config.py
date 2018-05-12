from api.bucket import app
from flask_testing import TestCase
import unittest


class TestDevelopmentEnvironment(TestCase):
    """ Test app in development environment"""
    def create_app(self):
        app.config.from_object('instance.config.DevelopmentEnvironment')
        return app

    def test_app_in_development(self):
        """ Should return true if debug is enabled"""
        self.assertTrue(app.config['DEBUG'])


class TestProductionEnvironment(TestCase):
    """Test app in production environment"""
    def create_app(self):
        app.config.from_object('instance.config.ProductionEnvironment')
        return app

    def test_app_in_production(self):
        """ Test if debug and testing are set to false"""
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])


class TestTestingEnvironment(TestCase):
    """Test app in testing environment"""
    def create_app(self):
        app.config.from_object('instance.config.TestingEnvironment')
        return app

    def test_app_in_testing(self):
        """ Test if debug and testing are set to true"""
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])


class TestStagingEnvironment(TestCase):
    """ Test app in staging environment"""
    def create_app(self):
        app.config.from_object('instance.config.StagingConfig')
        return app

    def test_app_in_testing(self):
        """ Check if debug is se to true"""
        self.assertTrue(app.config['DEBUG'])

if __name__ == '__main__':
    unittest.main()

# /instance/config.py

import os


class MainConfiguration(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentEnvironment(MainConfiguration):
    """Configurations for Development."""
    DEBUG = True


class TestingEnvironment(MainConfiguration):
    """Configurations for Testing."""
    TESTING = True
    DEBUG = True


class StagingConfig(MainConfiguration):
    """Configurations for Staging."""
    DEBUG = True


class ProductionEnvironment(MainConfiguration):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

# Dictionary of different configuration environments
application_config = {
    'MainConfig': MainConfiguration,
    'TestingEnv': TestingEnvironment,
    'DevelopmentEnv': DevelopmentEnvironment,
    'ProductionEnv': ProductionEnvironment
}

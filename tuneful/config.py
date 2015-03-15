# Need to resolve users in db, for now no username/password works
# To run this I need to load the Postgres app

# todo: Figure out how to create a user and password in both postgres and python code.
class DevelopmentConfig(object):
    USER = "michael"
    PASSWORD = "my_password"
    DATABASE_URI = "postgresql://:@localhost:5432/tuneful"
    DEBUG = True
    UPLOAD_FOLDER = "uploads"

class TestingConfig(object):
    DATABASE_URI = "postgresql://:@localhost:5432/tuneful-test"
    DEBUG = True
    UPLOAD_FOLDER = "test-uploads"

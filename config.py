import os

basedir = os.path.abspath(os.path.dirname(__file__))


# TODO: Switch to postgresql
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

# TODO: What does this do?
SQLALCHEMY_TRACK_MODIFICATIONS = False

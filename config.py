import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "NO_KEY"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
                              or 'sqlite:///' + os.path.join(basedir, 'app.db')
                              # or "jdbc: sqlite:/home/fares/PycharmProjects/blog/app.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

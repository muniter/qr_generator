import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'golf-alfa-bravo-Kilo-uniform\
        -victor-tango-uniform-sierra'

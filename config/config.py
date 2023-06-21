import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dgfh53tFh_T;nerDG$HNSrlm3kndklfgnlernhghg'


class KochbarConfig:
    USER = 'root'
    PASSWORD = ''
    HOST = '127.0.0.1'
    PORT = 3306
    DATABASE = 'crs_kochbar_slim'


import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    # CELERY_RESULT_BACKEND = "redis://localhost:6379"
    # CELERY_BROKER_URL = "redis://localhost:6379"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


languages = ["Python", "Java", "Go", "C#",
             "JavaScript", "Any", "TypeScript", "Bash"]
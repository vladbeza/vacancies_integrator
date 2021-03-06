import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
                        or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    result_backend = os.environ.get("CELERY_RESULT_BACKEND",
                                    "redis://localhost:6379")
    broker_url = os.environ.get("CELERY_BROKER_URL",
                                       "redis://localhost:6379")
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_SLOW_DB_QUERY_TIME = 1


location_translations = {"Харьков": ("харьков", "харків", "kharkiv", "kharkov"),
                        "Киев": ("киев", "київ", "kiyv", "kiev"),
                        "Львов": ("львов", "львів", "lviv"),
                        "Удаленно": ("удаленно", "remote", "віддалена робота")}


languages = ["Python", "Java", "Go", "C#",
             "JavaScript", "Any", "TypeScript", "Bash"]


skills = ["pytest", "big data", "machine learning", "junit", "unittest",
          "data analysis", "cucumber", "bdd", "tdd", "behave", "jmeter",
          "locust", "locustio", "mocha", "protractor", "jasmine", "jest",
          "karma", "robot framework", "appium", "selenide", "selenoid",
          "selenium", "api", "pyunit", "postman", "lettuce", "xcuitest",
          "xcode", "jtest", "testng", "cypress", "cypress.io", "winrunner",
          "silk test", "qtp", "applitools", "saucelabs", "testim",
          "sealights", "test.ai", "mabl", "retest", "reportportal",
          "artificial intelligence", "sikuli", "webdriver", "selenium grid",
          "aws", "penetration", "soapui", "rest-assured", "hp loadrunner",
          "docker", "kubernetes", "python", "java", "javascript/js",
          "c#/.net", "typescript", "bash", "jira", "nightwatch.js",
          "rest", "soap", "golang", "nunit", "ruby", "scala", "rust",
          "graphql", "security", "katalon studio", "webdriverio", "testcafe",
          "aerokube", "web", "mobile", "desktop"]

CITIES = ["Харьков", "Киев", "Одесса", "Львов", "Другой"]

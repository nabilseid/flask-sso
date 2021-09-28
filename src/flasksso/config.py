class Config(object):
    DEBUG = False
    TESTING = False
    POLICYCHECKTOGGLE = True

class ProductionConfig(Config):
    ssoURL = "https://api.sso.adludio.com"

class StagingConfig(Config):
    ssoURL = "https://staging.sso.adludio.com"

class DevelopmentConfig(Config):
    DEBUG = True
    ssoURL = "https://dev.api.sso.adludio.com"

class TestingConfig(Config):
    TESTING = True
    ssoURL = "https://testing.api.sso.adludio.com"

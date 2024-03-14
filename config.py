from datetime import timedelta


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = None
    PRESERVE_CONTEXT_ON_EXCEPTION = None
    SECRET_KEY = None
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    USE_X_SENDFILE = False
    LOGGER_NAME = None
    LOGGER_HANDLER_POLICY = 'always'
    SERVER_NAME = None
    APPLICATION_ROOT = None
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_PATH = None
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_REFRESH_EACH_REQUEST = True
    MAX_CONTENT_LENGTH = None
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(hours=12)
    TRAP_BAD_REQUEST_ERRORS = False
    TRAP_HTTP_EXCEPTIONS = False
    EXPLAIN_TEMPLATE_LOADING = False
    PREFERRED_URL_SCHEME = 'http'
    JSON_AS_ASCII = True
    JSON_SORT_KEYS = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    TEMPLATES_AUTO_RELOAD = None


class DevelopmentConfig(BaseConfig):
    JSON_AS_ASCII = False
    DEBUG = True
    SECRET_KEY = 'LanSenLin'

    # sqlalchemy 设置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:202030481266@117.72.36.19:3306/WebDemoDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20  # 设置并发池的大小
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    FLASK_ADMIN_SWATCH = 'cerulean'





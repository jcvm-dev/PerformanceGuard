import os

class Config:
    # Configurações básicas
    DEBUG = False
    TESTING = False
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/database/metrics.db')
    
    # Configurações de análise
    RESPONSE_TIME_THRESHOLD = 1000  # ms
    SECURITY_CHECK_ENABLED = True
    
    # Configurações de cache
    CACHE_ENABLED = True
    CACHE_TIMEOUT = 300  # segundos

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DATABASE_PATH = ':memory:'

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
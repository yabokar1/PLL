import os 
class AppConfig:
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    API_KEY = os.environ.get('OPEN_AI')
    ANALYZE_URL = os.environ.get('ANALYZE_URL')
    ANONYMIZE_URL = os.environ.get('ANONYMIZE_URL')
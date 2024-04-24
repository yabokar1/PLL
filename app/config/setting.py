import os 
class AppConfig:
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    API_KEY = os.environ.get('OPEN_AI')
    API_KEY = os.environ.get('API_KEY')
    ANALYZE_URL = os.environ.get('ANALYZE_URL')
    ANONYMIZE_URL = os.environ.get('ANONYMIZE_URL')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    OUTPUT_FILE = os.environ.get('OUTPUT_FILE')
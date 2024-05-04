import os 
class AppConfig:
    MONGO_USER = os.environ.get('MONGO_USER')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    OPEN_API_KEY = os.environ.get('OPEN_API_KEY')
    ANALYZE_URL = os.environ.get('ANALYZE_URL')
    ANONYMIZE_URL = os.environ.get('ANONYMIZE_URL')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    OUTPUT_FILE = os.environ.get('OUTPUT_FILE')
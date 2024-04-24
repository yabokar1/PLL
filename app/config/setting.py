import os 
class AppConfig:
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    API_KEY = os.environ.get('OPEN_AI')
    API_KEY = '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'
    ANALYZE_URL = os.environ.get('ANALYZE_URL')
    ANONYMIZE_URL = os.environ.get('ANONYMIZE_URL')
    AWS_ACCESS_KEY_ID = 'AKIAY4ZAXZ366WHTJTC2'
    AWS_SECRET_ACCESS_KEY = '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'
    S3_BUCKET_NAME = 'pllbucket1'
    OUTPUT_FILE = 'output.json'
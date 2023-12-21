import os 
class AppConfig:
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    API_KEY = os.environ.get('OPEN_AI')
    ANALYZE_URL = 'http://localhost:5001/analyze'
    ANONYMIZE_URL = 'http://localhost:5002/anonymize'
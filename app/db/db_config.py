import os 
class Config:
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
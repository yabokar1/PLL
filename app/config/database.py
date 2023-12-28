import sys
print(sys.path)
sys.path.append('/Users/yonisabokar/IBM_Data_AI/PLL')
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.config.setting import AppConfig



class Database:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.uri = f"mongodb+srv://{AppConfig.USER}:{AppConfig.PASSWORD}@cluster0.moujypz.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(self.uri, server_api=ServerApi('1'), tls=True, tlsAllowInvalidCertificates=True)

    def get_client(self):
        return self.client


    

if __name__ == "__main__":

    try:
         db = Database()
         client = db.get_client()
         client.admin.command('ping')
         print("Pinged your deployment. You successfully connected to MongoDB!")
         print("Database is created !!")
        #  user_collection = client['PLL']['Users']
        #  user_collection.insert_one({'firstname': 'Yonis',
        #                               'lastname': 'Abokar',
        #                               'username': 'yabokar',
        #                               'password': 'password'})

    except Exception as e:
            print(e)


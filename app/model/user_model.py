import sys
sys.path.append('/Users/yonisabokar/IBM_Data_AI/PLL')
from app.config.database import Database
from bson.objectid import ObjectId

class User:
    
    def __init__(self):
        self.db = Database().get_client()['PLL']['User']


    def save(self):
        data = {
            'firstname': "",
            'lastname': "",
            'username': "",
            'password': "",
        }
        result = self.db.insert_one(data)
        return str(result.inserted_id)
  
    def get_all_users(self):
        users = self.db.find()
        return [{'firstname': user['firstname'], 'lastname': user['lastname'], 'username': user['username'], 'password': 
                 user['password'] } for user in users]

    def get_user_by_credentials(self,username,password):
        user = self.db.find_one({'username': username, 'password': password})
        return user

    def update_user(self,id,user_update):
        message = self.get_user_by_name(id)
        result = self.table.collection.update_one(message,user_update)
        return result.modified_count > 0

    def delete(self,username):
        result = self.delete_one({'username': username})
        return result.deleted_count > 0
    


if __name__ == "__main__":

    try:
        username = ''
        user_table = User()
        user_messages = user_table.get_all_users()
        print(user_messages)
        message = user_table.get_user_by_name(id)
        print(message)

    except Exception as e:
            print(e)
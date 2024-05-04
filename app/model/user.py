from app.config.database import Database
import bcrypt

class User:
    def __init__(self):
        self.db = Database().get_client()['PLL']['User']

    def save(self,firstname,lastname,username,password):
        password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        data = {
            'firstname': firstname,
            'lastname': lastname,
            'email': username,
            'password': hashed_password,
        }
        result = self.db.insert_one(data)
        return str(result.inserted_id)
  
    def get_all_users(self):
        users = self.db.find()
        return [{'firstname': user['firstname'], 'lastname': user['lastname'], 'email': user['email'], 'password': 
                 user['password'] } for user in users]

    def get_credentials(self,username):
        user = self.db.find_one({'email': username})
        return user

    def update_user(self,id,user_update):
        message = self.get_user_by_name(id)
        result = self.table.collection.update_one(message,user_update)
        return result.modified_count > 0

    def delete(self,username):
        result = self.delete_one({'email': username})
        return result.deleted_count > 0
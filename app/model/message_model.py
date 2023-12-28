import sys
# sys.path.append('/Users/yonisabokar/IBM_Data_AI/PLL')
from app.config.database import Database
from bson.objectid import ObjectId

class Message:
    
    def __init__(self):
        self.db = Database().get_client()['PLL']['Messages']


    def save(self,anonmyized, deanonmyized):
        data = {
            'anonmyized': anonmyized,
            'deanonmyized': deanonmyized
        }
        result = self.db.insert_one(data)
        return str(result.inserted_id)
  
    def get_all_messages(self):
        messages = self.db.find()
        return [{'anonmyized': message['anonmyized'], 'deanonmyized': message['deanonmyized']} for message in messages]

    def get_message_by_id(self,id):
        object_id = ObjectId(id)
        message = self.db.find_one({'_id': object_id})
        return message

    def update_message(self,id,new_message):
        message = self.get_message_by_id(id)
        result = self.table.collection.update_one(message,new_message)
        return result.modified_count > 0

    def delete(self,id):
        object_id = ObjectId(id)
        result = self.table.collection.delete_one({'id': object_id})
        return result.deleted_count > 0
    


if __name__ == "__main__":

    try:
        id = '6583490f07593d94c553543f'
        message_table = Message()
        user_messages = message_table.get_all_messages()
        print(user_messages)
        message = message_table.get_message_by_id(id)
        print(message)

    except Exception as e:
            print(e)
from chat_app.database_operations.models import UserTable
from chat_app import login

class User:
    """a wrapper for UserTable that can be used with the flask-login extension"""
    def __init__(self, username, display_name, email_address, datetime_joined, password_hash, is_authenticated_field, is_active_field, is_anonymous_field):
        self.username = username
        self.display_name = display_name
        self.email_address = email_address
        self.password_hash = password_hash
        self.datetime_joined = datetime_joined
        
        self.is_authenticated_field = is_authenticated_field
        self.is_active_field = is_active_field
        self.is_anonymous_field = is_anonymous_field
    
    def get_id(self):
        return self.username
    
    def is_authenticated(self):
        return self.is_authenticated_field
    
    def is_active(self):
        return self.is_active_field
    
    def is_anonymous(self):
        return self.is_anonymous_field


@login.user_loader
def load_user(username):
    user_record = UserTable.get_user_record_by_username(username)
    user = User(user_record['username'], user_record['display_name'], user_record['email_address'], user_record['datetime_joined'], \
        user_record['password_hash'], user_record['is_authenticated'], user_record['is_active'], user_record['is_anonymous'])
    return user

#print(load_user('avinash')) # should print User object

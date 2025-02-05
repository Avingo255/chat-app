from werkzeug.security import generate_password_hash
from chat_app.database_operations.cloud_database import query_db #use this when running server
#from cloud_database import query_db #use this when running this file on its own

import datetime

class UserTable:
    """Represents user table in database1"""   
    INVALID_FIELD_VALUES = [None, '']
    
    @staticmethod
    def get_all_usernames() -> list:
        """returns list of all usernames"""
        result = query_db("SELECT username FROM user;")
        if result == None:
            return []
        else:
            to_return = []
            for each_tuple in result:
                to_return.append(each_tuple[0])
            return to_return
        
    @staticmethod
    def get_number_of_users() -> int:
        """Returns number of users in user table"""
        result = query_db("SELECT COUNT(username) FROM user;")
        return result[0][0]
        
        
    @staticmethod
    def validate_password(raw_password: str) -> list:        
        """_summary_
        Validates password based on criteria: Length must be at least 12 chars, must contain at least one numerical 
        digit, must contain at least one capital letter, must contain at least one lowercase letter, must contain at 
        least one special character in !@#$%^&*()-_+=[]{}|;:,.<>?/~`.
        
        Args:
            raw_password (str): password to validate
        
        Returns:
            list: index 0: True if password is valid, False otherwise
                  index 1: list of reasons why password is invalid (if password is invalid)
        """
            
        reasons = []
            
        if len(raw_password) < 12:
            reasons.append("Password must be at least 12 characters long.")
            
        if not any(char.isdigit() for char in raw_password):
            reasons.append("Password must contain at least one numerical digit.")
        
        if not any(char.isupper() for char in raw_password):
            reasons.append("Password must contain at least one capital letter.")
            
        if not any(char.islower() for char in raw_password):
            reasons.append("Password must contain at least one lowercase letter.")
            
        if not any(char in '!@#$%^&*()-_+=[]{}|;:,.<>?/~`' for char in raw_password):
            reasons.append("Password must contain at least one special character in !@#$%^&*()-_+=[]{}|;:,.<>?/~`.")
        
        if reasons == []:
            return [True]
        else:
            return [False, reasons]
        
        
    @staticmethod
    def check_email_address_valid(email_address: str) -> list:
        """Checks if email address is valid
        
        Args:
            email_address (str): email address to check
        
        Returns:
            list: index 0: True if email address is valid, False otherwise
                    index 1: invalid email address error message
        """
        invalid_email_address_message = "Error: Invalid email address: Must have exactly one '@' and at least one '.' character."
        return ['@' in email_address and '.' in email_address and email_address.count('@') == 1, invalid_email_address_message]

    
    # CREATE
    @staticmethod
    def create_user(username: str, display_name: str, email_address: str, raw_password: str) -> None:
        """_summary_
        Creates a user in the user table - calling context must specify username, display_name, email_address, and raw_password
        
        Args:
            username (str): username (PK) of user
            display_name (str): display name of user
            email_address (str): email address of user, must meet criteria specified by UserTable.check_email_address_valid
            raw_password (str): raw password of user, must meet criteria specified by UserTable.validate_password
        
        Raises:
            Exception: username, display_name, email_address, or raw_password is empty
            Exception: email_address is invalid
            Exception: password is invalid
            Exception: username already exists
        
        Returns:
            None
        """
        if username in UserTable.INVALID_FIELD_VALUES or display_name in UserTable.INVALID_FIELD_VALUES or email_address \
            in UserTable.INVALID_FIELD_VALUES or raw_password in UserTable.INVALID_FIELD_VALUES:
            raise Exception("Error: A field value is empty.")
        
        elif not UserTable.check_email_address_valid(email_address)[0]:
            raise Exception(UserTable.check_email_address_valid(email_address)[1])
        
        elif UserTable.validate_password(raw_password)[0] == False:
            raise Exception(f"Error: Invalid password: {UserTable.validate_password(raw_password)[1]}")

        elif username not in UserTable.get_all_usernames() or UserTable.get_all_usernames() == []:
            parameter_dictionary = {
                'username': username,
                'display_name': display_name,
                'email_address': email_address,
                'password_hash': generate_password_hash(raw_password)
            }
            query = """
            INSERT INTO database1.user (username, display_name, email_address, password_hash)
            VALUES (:username, :display_name, :email_address, :password_hash);
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
        else:
            raise Exception(f"Error: Username '{username}' already exists.")
        
    
    #READ
    @staticmethod
    def get_user_record_by_username(username: str) -> dict:
        """_summary_
        Returns dictionary of user data for a given username
        
        Args:
            username (str): username (PK) of record in User table to be accessedd
        
        Raises:
            Exception: username is empty
            Exception: username not in table

        Returns:
            dict: dictionary of user data (username, display_name, email_address, datetime_joined, password_hash, is_authenticated, is_active, is_anonymous)
        """
        
        if username in UserTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Username cannot be empty.")
        elif username not in UserTable.get_all_usernames():
            raise Exception(f"Error: User '{username}' does not exist.")
        else:
            parameter_dictionary = {
                'username': username
            }
            raw_tuple_output = query_db(f"SELECT * FROM database1.user WHERE username = :username;", parameter_dictionary=parameter_dictionary)[0]
            
            dictionary_output = {
                'username': raw_tuple_output[0],
                'display_name': raw_tuple_output[1],
                'email_address': raw_tuple_output[2],
                'datetime_joined': raw_tuple_output[3],
                'password_hash': raw_tuple_output[4],
                'is_authenticated': raw_tuple_output[5],
                'is_active': raw_tuple_output[6],
                'is_anonymous': raw_tuple_output[7]
            }
            return dictionary_output 
        
    @staticmethod
    def check_user_in_group(username: str, group_id: int) -> bool:
        """_summary_
        Checks if user with username is in group with group_id
        
        Args:
            username (str): username (PK) of user
            group_id (int): group_id (PK) of group
        
        Returns:
            bool: True if user is in group, False otherwise
        """
        if username in UserTable.INVALID_FIELD_VALUES or group_id in UserTable.INVALID_FIELD_VALUES:
            raise Exception("Error: A field value is empty.")
        elif username not in UserTable.get_all_usernames():
            raise Exception(f"Error: User '{username}' does not exist.")
        elif group_id not in GroupTable.get_all_group_ids():
            raise Exception(f"Error: Group '{group_id}' does not exist.")
        else:
            query = """
            SELECT COUNT(*) 
            FROM 
                database1.user_group, 
                database1.user, 
                database1.group 
            WHERE user.username = :username
            AND group.group_id = :group_id
            AND user_group.username = user.username
            AND user_group.group_id = group.group_id;
            """
            parameter_dictionary = {
                'username': username,
                'group_id': group_id
            }
            result = query_db(query, parameter_dictionary=parameter_dictionary)
            return result[0][0] == 1
    
    
    @staticmethod
    def get_user_groups(username: str) -> dict:
        """_summary_
        Returns dict of group_id, group_name, any_messages, last_message_user_display_name, last_message, last_message_datetime for all groups user is in
        
        Args:
            username (str): username (PK) of user to get groups for
        
        Raises:
            Exception: username is empty
            Exception: username not in table

        Returns:
            dict: group_id, group_name, any_messages, last_message_user_display_name, last_message, last_message_datetime for all groups user is in
            \nif any_messages is False, last_message_user_display_name, last_message, last_message_datetime will be None
        """
        
        if username in UserTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Username cannot be empty.")
        elif username not in UserTable.get_all_usernames():
            raise Exception(f"Error: User '{username}' does not exist.")
        else:
            query = """
            WITH recent_messages AS (
                SELECT 
                    m.group_id,
                    m.message_content,
                    m.sender_username,
                    m.message_date_time,
                    ROW_NUMBER() OVER (PARTITION BY m.group_id ORDER BY m.message_date_time DESC) AS rn
                FROM 
                    database1.message m
            ),
            group_message_status AS (
                SELECT 
                    g.group_id,
                    g.group_name,
                    u.username,
                    COALESCE(rm.message_content, '') AS last_message_content,
                    COALESCE(rm.message_date_time, NULL) AS last_message_date_time,
                    COALESCE(ud.display_name, '') AS last_message_user_display_name,
                    CASE WHEN COUNT(m.message_id) OVER (PARTITION BY g.group_id) > 0 THEN TRUE ELSE FALSE END AS any_messages
                FROM 
                    database1.group g
                JOIN 
                    database1.user_group ug ON g.group_id = ug.group_id
                JOIN 
                    database1.user u ON ug.username = u.username
                LEFT JOIN 
                    recent_messages rm ON g.group_id = rm.group_id AND rm.rn = 1
                LEFT JOIN 
                    database1.user ud ON rm.sender_username = ud.username
                LEFT JOIN 
                    database1.message m ON g.group_id = m.group_id
                WHERE 
                    u.username = :username
            )
            SELECT DISTINCT
                group_id,
                group_name,
                any_messages,
                last_message_user_display_name,
                last_message_content,
                last_message_date_time
            FROM 
                group_message_status;

            """
        
            parameter_dictionary = {
                'username': username
            }
            results = query_db(query, parameter_dictionary=parameter_dictionary)
            group_info = []
            
            for result in results:
                                 
                group_info.append({
                    "group_id": result[0],
                    "group_name": result[1],
                    "any_messages": result[2],
                    "last_message_user_display_name": result[3] if result[2] != 0 else None,
                    "last_message": result[4] if result[2] != 0 else None,
                    "last_message_datetime": result[5].strftime('%d/%m/%y') if result[2] != 0 else None
                })
            return group_info
        
        
    @staticmethod
    def get_pending_invite_requests(username: str) -> list:
        """_summary_
        Returns list of tuples of pending invite request records for a given username
        
        Args:
            username (str): username (PK) of user to get pending invite requests for
        
        Raises:
            Exception: username is empty
            Exception: username not in table
        
        Returns:
            list: list of all pending invite request records for specified username"""
        
        if username in UserTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Username cannot be empty.")
        elif username not in UserTable.get_all_usernames():
            raise Exception(f"Error: User '{username}' does not exist.")
        else:
            query = """
            SELECT 
                invite_request.request_id,
                invite_request.receiver_username,
                invite_request.sender_username,
                invite_request.group_id,
                invite_request.status,
                invite_request.request_date_time
                
            FROM
                database1.invite_request, database1.user
            WHERE
                receiver_username = :username
                AND status = 'pending'
                AND invite_request.receiver_username = user.username
                AND user.username = :username;
            """
            
            
            parameter_dictionary = {
                'username': username
            }
            #raw_tuple_output = query_db("SELECT * FROM database1.invite_request,  WHERE invite_request.receiver_username = :username \
             #   AND status = 'pending';", parameter_dictionary=parameter_dictionary)
            raw_tuple_output = query_db(query, parameter_dictionary=parameter_dictionary)
            requests = []
            for each_tuple in raw_tuple_output:
                requests.append(each_tuple)
            return requests
        
        
    #UPDATE
    @staticmethod
    def update_existing_user_field(username: str, field: str, new_value: str) -> None:
        """field can be 'username', 'display_name', 'email_address', 'password_hash', 'is_authenticated', 'is_active'
        if field to update is 'password_hash', new_value can be raw password
        cannot update 'datetime_joined' or 'is_anonymous' fields
        Note: even if new_value is a boolean, it must be passed as a string for the sql query to work"""
        
        """_summary_
        Updates a field in the user table for a given username
        
        Args:
            username (str): username (PK) of user to update
            field (str): field to update, must be one of: [username, display_name, email_address, password_hash, is_authenticated, is_active]
            new_value (str): new value to update field with
            
        Raises: 
            Exception: field is invalid
            Exception: new_value is empty
            Exception: email_address is invalid
            Exception: username already exists
            Exception: display_name has not changed
        
        Returns:
            None
        """
        
        #1. VALIDATE
        if field not in ['username', 'display_name', 'email_address', 'password_hash', 'is_authenticated', 'is_active']: #check if field is valid
            raise Exception("Error: Invalid field name. Field name must be one of [username, display_name, email_address, password_hash, is_authenticated, is_active].\
                Cannot update 'datetime_joined' or 'is_anonymous'.")
        
        elif new_value in UserTable.INVALID_FIELD_VALUES: #check if new value is empty
            raise Exception("Error: New field value cannot be empty.")
        
        elif field == 'password_hash': #hash new password
            new_value = generate_password_hash(new_value)
            
        elif field == 'email_address': #check email address valid
            if not UserTable.check_email_address_valid(new_value)[0]:
                raise Exception("Error: Invalid email address.")
            
        elif username == new_value and field == 'username': #check username has changed
        #if condition field == 'username' was not present, user would not be able to have 
        # the same display name and username 
            raise Exception("Error: Username has not changed.")
               
        elif field == 'username': #check username unique
            if new_value in UserTable.get_all_usernames():
                raise Exception(f"Error: Username '{new_value}' already taken.")
            
        elif field == 'display_name' and new_value == UserTable.get_user_record_by_username(username)['display_name']: #check display name has changed
            raise Exception("Error: Display name has not changed.")
        
        elif field == 'email_address' and new_value == UserTable.get_user_record_by_username(username)['email_address']: #check email address has changed
            raise Exception("Error: Email address has not changed.")
        
        # do not check if password has changed, as this would effectively become a password check function            
        
        #2. NOW UPDATE
        elif username in UserTable.get_all_usernames():
            parameter_dictionary = {
                'username': username,
                'new_value': new_value
            }
            
            query = f"""
            UPDATE database1.user
            SET {field} = :new_value
            WHERE username = :username;
            """
            #here, field does not need to be sanitised as it is validated in the first if statement
            #sqlalchemy framework also does not support parameterising field names in queries
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
        else:
            raise Exception(f"Error: User '{username}' does not exist.")        
   
    
    #DELETE
    @staticmethod
    def delete_user(username: str) -> None:
        """_summary_
        Deletes a user from the user table
        
        Args:
            username (str): username (PK) of user to delete
        
        Raises:
            Exception: username is empty
            Exception: user does not exist
            
        Returns:
            None
        """
        if username in UserTable.get_all_usernames():
            parameter_dictionary = {
                'username': username
            }
            query = """
            DELETE FROM database1.user
            WHERE username = :username;
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
        else:
            raise Exception(f"Error: User '{username}' does not exist.")
        
class GroupTable:
    INVALID_FIELD_VALUES = [None, '']
    
    @staticmethod
    def get_all_group_ids():
        """returns list of all group_ids"""
        result = query_db("SELECT group_id FROM database1.group;")
        if result == None:
            return []
        else:
            to_return = []
            for each_tuple in result:
                to_return.append(each_tuple[0])
            return to_return
        
    @staticmethod
    def get_number_of_groups() -> int:
        """Returns number of groups in group table"""
        result = query_db("SELECT COUNT(group_id) FROM database1.group;")
        return result[0][0]
        
    @staticmethod
    def check_group_exists(group_id: int) -> bool:
        """_summary_
        Checks if group with group_id exists
        
        Args:
            group_id (int): primary key field of group table
        
        Returns:
            bool: True if group exists, False otherwise
        """
        return group_id in GroupTable.get_all_group_ids()
    
    @staticmethod
    def get_last_group_id():
        """_summary_
        Returns the last group_id that was created
        
        Returns:
            int: last group_id that was created
        """
        result = query_db("SELECT MAX(group_id) FROM database1.group;")
        
        return result[0][0]
    
    
    # CREATE
    @staticmethod
    def create_group(group_name: str) -> None:
        """_summary_
        Creates a group in the group table - calling context must specify group_name
        
        Args:
            group_name (str): name of group to create
            
        Raises:
            Exception: group_name is empty
        
        Returns:
            None
        """
        if group_name in GroupTable.INVALID_FIELD_VALUES:
            raise Exception("Error: A field value is empty.")

        else:
            parameter_dictionary = {
            'group_name': group_name
            }
        
            # group_id is autoincremented, so it does not need to be specified
            query = """
            INSERT INTO database1.group (group_name)
            VALUES (:group_name);
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
        
    # READ
    @staticmethod
    def get_group_record_by_group_id(group_id: int) -> dict:
        """_summary_
        returns dictionary of group data (group_id, group_name, datetime_created) for a given group_id
        
        Args:
            group_id (int): primary key field of group table
        
        Raises:
            Exception: group_id cannot be empty
            Exception: group with group_id does not exist
        
        Returns:
            dict: dictionary of group_id, group_name, datetime_created
        """
        if group_id in GroupTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Group ID cannot be empty.")
        elif group_id not in GroupTable.get_all_group_ids():
            raise Exception(f"Error: Group with '{group_id}' does not exist.")
        else:
            parameter_dictionary = {
                'group_id': group_id
            }
            
            raw_tuple_output = query_db("SELECT * FROM database1.group WHERE group_id = :group_id;", \
                parameter_dictionary=parameter_dictionary)[0]
            
            dictionary_output = {
                'group_id': raw_tuple_output[0],
                'group_name': raw_tuple_output[1],
                'datetime_created': raw_tuple_output[2]
            }
            return dictionary_output
    
    @staticmethod
    def get_number_of_users(group_id: int) -> int:
        """Returns number of users in a given group"""
        if group_id in GroupTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Group ID cannot be empty.")
        elif group_id not in GroupTable.get_all_group_ids():
            raise Exception(f"Error: Group with '{group_id}' does not exist.")
        else:
            parameter_dictionary = {
            'group_id': group_id
            }
            result = query_db("SELECT COUNT(username) FROM database1.user_group, database1.group WHERE user_group.group_id = :group_id AND group.group_id = user_group.group_id;", parameter_dictionary=parameter_dictionary)
            return result[0][0]
        
    @staticmethod
    def get_number_of_online_users(group_id: int) -> int:
        """Returns number of online users in a given group"""
        if group_id in GroupTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Group ID cannot be empty.")
        elif group_id not in GroupTable.get_all_group_ids():
            raise Exception(f"Error: Group with '{group_id}' does not exist.")
        else:
            parameter_dictionary = {
            'group_id': group_id
            }
            query = """
            SELECT COUNT(user_group.username) 
            FROM database1.user_group, database1.user, database1.group
            WHERE group.group_id = :group_id
            AND user_group.group_id = group.group_id
            AND user.username = user_group.username
            AND user.is_authenticated = 1;
            """
            result = query_db(query, parameter_dictionary=parameter_dictionary)
            return result[0][0]
        
    
    @staticmethod
    def get_group_users(group_id: int) -> list:
        """_summary_
        returns list of usernames in a given group with group_id
        
        Args:
            group_id (int): primary key field of group table
        
        Raises:
            Exception: group_id cannot be empty
            Exception: group with group_id does not exist
            
        Returns:
            list: list of all usernames of users in specified group with group_id   
        """
        if group_id in GroupTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Group ID cannot be empty.")
        
        elif group_id not in GroupTable.get_all_group_ids():
            raise Exception(f"Error: Group with '{group_id}' does not exist.")
        
        else:
            parameter_dictionary = {
                'group_id': group_id
            }
            raw_tuple_output = query_db("SELECT user_group.username FROM database1.user_group, database1.group WHERE user_group.group_id = :group_id AND user_group.group_id = group.group_id;", \
                parameter_dictionary=parameter_dictionary)
            users = []
            for each_tuple in raw_tuple_output:
                users.append(each_tuple[0])
            return users
        
    def get_group_user_details(group_id: int) -> dict:
        """_summary_
        Returns dictionary of username, user display name, is_authenticated for every user in the group

        Args:
            group_id (int): primary key field of group table

        Raises:
            Exception: group_id cannot be empty
            Exception: group with group_id does not exist

        Returns:
            dict: dictionary of username, user display name, is_authenticated for every user in the group
        """
        if group_id in GroupTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Group ID cannot be empty.")
        elif group_id not in GroupTable.get_all_group_ids():
            raise Exception(f"Error: Group with '{group_id}' does not exist.")
        else:
            parameter_dictionary = {
                'group_id': group_id
            }
            query = """
            SELECT 
                u.username, 
                u.display_name, 
                u.is_authenticated 
            FROM 
                database1.user_group ug
            JOIN 
                database1.user u 
                ON ug.username = u.username
            WHERE 
                ug.group_id = :group_id;
            """
            results = query_db(query, parameter_dictionary=parameter_dictionary)
            user_details = []
            for result in results:
                user_details.append({
                    "username": result[0],
                    "display_name": result[1],
                    "is_authenticated": result[2]
                })
            return user_details
    
    def get_group_datetime_created(group_id: int) -> str:
        """_summary_
        Returns the datetime_created for a given group_id
        
        Args:
            group_id (int): primary key field of group table
        
        Raises:
            Exception: group_id cannot be empty
            Exception: group with group_id does not exist
        
        Returns:
            datetime: datetime_created of the group
        """
        if group_id in GroupTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Group ID cannot be empty.")
        elif group_id not in GroupTable.get_all_group_ids():
            raise Exception(f"Error: Group with '{group_id}' does not exist.")
        else:
            parameter_dictionary = {
                'group_id': group_id
            }
            result = query_db("SELECT datetime_created FROM database1.group WHERE group_id = :group_id;", parameter_dictionary=parameter_dictionary)
            return result[0][0].strftime('%d/%m/%y %H:%M:%S')
    
    
    @staticmethod
    def get_all_group_messages(group_id: int) -> list:
        """_summary_ 
        returns message records (as tuples) in a given group with group_id ordered by message_date_time (oldest messages first)
        tuple format: (messaage_id, message_content, message_date_time, sender_username, sender_display_name)
        
        Args:
            group_id (int): primary key field of group table
            
        Raises:
            Exception: group_id cannot be empty
            Exception: group with group_id does not exist
        
        Returns:
            list: list of all message records in specified group with group_id, along with sender display name
        """
        if group_id in GroupTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Group ID cannot be empty.")
        elif group_id not in GroupTable.get_all_group_ids():
            raise Exception(f"Error: Group with '{group_id}' does not exist.")
        else:
            parameter_dictionary = {
                'group_id': group_id
            }
            query = """
            SELECT
                m.message_id,
                m.message_content,
                m.message_date_time,
                m.sender_username,
                u.display_name
            FROM 
                database1.message AS m
            JOIN 
                database1.user AS u 
                ON m.sender_username = u.username
            WHERE 
                m.group_id = :group_id
            ORDER BY 
                m.message_date_time ASC;
            """
            #raw_tuple_output = query_db(f"SELECT * FROM database1.message WHERE group_id = :group_id ORDER BY message_date_time ASC;", parameter_dictionary=parameter_dictionary)
            raw_tuple_output = query_db(query, parameter_dictionary=parameter_dictionary)
            messages = []
            for each_tuple in raw_tuple_output:
                messages.append(each_tuple)
            return messages
        
    @staticmethod
    def get_latest_group_message(group_id: int) -> tuple:
        """_summary_
        returns latest message record in a given group with group_id
        tuple format: (message_id, message_content, message_date_time, sender_username, sender_display_name)
        
        Args:
            group_id (int): primary key field of group table
            
        Raises:
            Exception: group_id cannot be empty
            Exception: group with group_id does not exist
        
        Returns:
            tuple: latest message record in specified group with group_id, along with sender display name
        """
        if group_id in GroupTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Group ID cannot be empty.")
        elif group_id not in GroupTable.get_all_group_ids():
            raise Exception(f"Error: Group with '{group_id}' does not exist.")
        else:
            parameter_dictionary = {
                'group_id': group_id
            }
            query = """
            SELECT 
                m.message_id,
                m.message_content,
                m.message_date_time,
                m.sender_username,
                u.display_name
            FROM 
                database1.message AS m
            JOIN 
                database1.user AS u 
                ON m.sender_username = u.username
            WHERE 
                m.group_id = :group_id
            ORDER BY 
                m.message_date_time DESC
            LIMIT 1;
            """
            raw_tuple_output = query_db(query, parameter_dictionary=parameter_dictionary)
            return raw_tuple_output
    
    
    # UPDATE
    @staticmethod
    def update_group_name(group_id: int, new_group_name: str) -> None:
        """_summary_
        Updates group_name field in group table for a given group_id
        
        Args:
            group_id (int): primary key field of group table
            new_group_name (str): new group name to update group with
            
        Raises:
            Exception: group_id or new_group_name is empty
            Exception: group name has not changed
            Exception: group with group_id does not exist
            
        Returns:
            None        
        """
        parameter_dictionary = {
            'group_id': group_id,
            'new_group_name': new_group_name
        }
        
        if group_id in GroupTable.INVALID_FIELD_VALUES or new_group_name in GroupTable.INVALID_FIELD_VALUES: #check if new value is empty
            raise Exception("Error: New field value cannot be empty.")
            
        elif new_group_name == GroupTable.get_group_record_by_group_id(group_id)['group_name']: #check group name has changed
            raise Exception("Error: Group name has not changed.") 
        
        elif group_id in GroupTable.get_all_group_ids():
            query = """
            UPDATE database1.group
            SET group_name = :new_group_name
            WHERE group_id = :group_id;
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
        
        else:
            raise Exception(f"Error: Group with '{group_id}' does not exist.")   
    
    
    # DELETE
    @staticmethod
    def delete_group(group_id: int) -> None:
        """_summary_
        Deletes a group from the group table with a given group_id
        
        Args:
            group_id (int): primary key field of group table
            
        Raises:
            Exception: group_id is empty
            Exception: group with group_id does not exist
            
        Returns:
            None        
        """
        if group_id in GroupTable.get_all_group_ids():
            parameter_dictionary = {
                'group_id': group_id
            }
            
            query = """
            DELETE FROM database1.group
            WHERE group_id = :group_id;
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
        else:
            raise Exception(f"Error: Group  with'{group_id}' does not exist.")



class UserGroupTable:
    INVALID_FIELD_VALUES = [None, '']
    #read methods will be part of the User and Group classes
    #as they are more relevant to those classes
    #no point having update methods
    
    @staticmethod
    def get_all_user_group_ids() -> list:
        """_summary_
        Returns list of all user_group_ids
        Returns:
            list: all user_group_ids (PK for user_group table)
        """
        query = "SELECT username, group_id FROM database1.user_group;"
        result = query_db(query)
        return [list(row) for row in result]
    
    
    @staticmethod
    def create_user_group(username: str, group_id: int) -> None:
        """_summary_
        Creates a user_group record in the user_group table - calling context must specify username and group_id
        
        Args:
            username (str): username (PK) of user table
            group_id (int): group_id (PK) of group table
            
        Raises:
            Exception: username or group_id is empty
            Exception: user with username does not exist
            Exception: group with group_id does not exist
            Exception: user with username is already in group with group_id
        
        Returns:
            None
        """
        if username in UserGroupTable.INVALID_FIELD_VALUES or group_id in UserGroupTable.INVALID_FIELD_VALUES:
            raise Exception("Error: A field value is empty.")
        
        elif username not in UserTable.get_all_usernames():
            raise Exception(f"Error: User '{username}' does not exist.")
        
        elif group_id not in GroupTable.get_all_group_ids():
            raise Exception(f"Error: Group '{group_id}' does not exist.")
        
        elif [username, group_id] in UserGroupTable.get_all_user_group_ids():
            raise Exception(f"Error: User '{username}' is already in group '{group_id}'.")
        
        else:
            parameter_dictionary = {
                'username': username,
                'group_id': group_id
            }
            query = """
            INSERT INTO database1.user_group (username, group_id)
            VALUES (:username, :group_id);
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
    
    
    @staticmethod
    def delete_user_group(username, group_id):
        """_summary_
        Deletes a user_group record in the user_group table - calling context must specify username and group_id
        
        Args:
            username (str): username (PK) of user table
            group_id (int): group_id (PK) of group table
            
        Raises:
            Exception: username or group_id is empty
            Exception: user with username is not in group with group_id (no such record to delete)
            
        Returns:
            None
        """
        if username in UserGroupTable.INVALID_FIELD_VALUES or group_id in UserGroupTable.INVALID_FIELD_VALUES:
            raise Exception("Error: A field value is empty.")
        elif UserTable.check_user_in_group(username, group_id) == False:
            raise Exception(f"Error: User '{username}' is not in group '{group_id}'.")
        else:
            parameter_dictionary = {
                'username': username,
                'group_id': group_id
            }
            query = """
            DELETE FROM database1.user_group
            WHERE username = :username AND group_id = :group_id;
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
    


class MessageTable:
    INVALID_FIELD_VALUES = [None, '']
    MAX_MESSAGE_LENGTH = 2000
    
    @staticmethod
    def get_all_message_ids() -> list:
        """_summary_ 
        returns list of all message_ids
        Returns:
            list: all message_ids (PK for message table)
        """
        result = query_db("SELECT message_id FROM database1.message;")
        if result == None:
            return []
        else:
            all_message_ids = []
            for each_tuple in result:
                all_message_ids.append(each_tuple[0])
            return all_message_ids
    
    @staticmethod
    def get_number_of_messages() -> int:
        """_summary_
        Returns number of messages in message table
        Returns:
            int: number of messages in message table
        """
        result = query_db("SELECT COUNT(message_id) FROM database1.message;")
        return result[0][0]
    
    @staticmethod
    def create_message(message_content: str, sender_username: str, group_id: int) -> None:
        """_summary_
        Creates a message in the message table - calling context must specify message_content, sender_username, and group_id
        
        Args:
            message_content (str): Message text (must be <= MessageTable.MAX_MESSAGE_LENGTH (2000) characters)
            sender_username (str): username (PK) of message sender 
            group_id (int): group_id (PK) of group message is sent in

        Raises:
            Exception: message_content length is > MessageTable.MAX_MESSAGE_LENGTH (2000) characters
            Exception: message_content, sender_username, or group_id is empty
            Exception: user with sender_username does not exist
            Exception: group with group_id does not exist
            Exception: user with sender_username is not in group with group_id

        Returns:
            None
        """
        if len(message_content) > MessageTable.MAX_MESSAGE_LENGTH:
            raise Exception("Error: Message text is too long.")
        
        elif message_content in MessageTable.INVALID_FIELD_VALUES or sender_username in MessageTable.INVALID_FIELD_VALUES \
            or group_id in MessageTable.INVALID_FIELD_VALUES:
            raise Exception("Error: A field value is empty.") #No empty messages, senders, or groups
        
        elif sender_username not in UserTable.get_all_usernames():
            raise Exception(f"Error: User '{sender_username}' does not exist.")
        
        elif group_id not in GroupTable.get_all_group_ids():
            raise Exception(f"Error: Group with group_id '{group_id}' does not exist.")
        
        elif UserTable.check_user_in_group(sender_username, group_id) == False:
            raise Exception(f"Error: User '{sender_username}' is not in group '{group_id}'.")
        
        else:
            parameter_dictionary = {
                'message_content': message_content,
                'sender_username': sender_username,
                'group_id': group_id
            }
            query = """
            INSERT INTO database1.message (message_content, sender_username, group_id)
            VALUES (:message_content, :sender_username, :group_id);
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
    
    
    @staticmethod
    def get_message_record_by_message_id(message_id: int) -> dict:
        """_summary_
        returns dictionary of message data for a given message_id
        
        Args:
            message_id (int): primary key field of message table

        Raises:
            Exception: message_id cannot be empty
            Exception: a message with message_id does not exist

        Returns:
            dictionary_output (dict): of message_id, message_content, message_date_time, sender_username, group_id
        """
        if message_id in MessageTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Message ID cannot be empty.")
        elif message_id not in MessageTable.get_all_message_ids():
            raise Exception(f"Error: Message with message_id '{message_id}' does not exist.")
        else:
            parameter_dictionary = {
                'message_id': message_id
            }
            raw_tuple_output = query_db(f"SELECT * FROM database1.message WHERE message_id = :message_id;", \
                parameter_dictionary=parameter_dictionary)[0]
            
            dictionary_output = {
                'message_id': raw_tuple_output[0],
                'message_content': raw_tuple_output[1],
                'message_date_time': raw_tuple_output[2],
                'sender_username': raw_tuple_output[3],
                'group_id': raw_tuple_output[4]
            }
            return dictionary_output
    
    
    @staticmethod
    def update_message_content(message_id: int, new_message_content):        
        if message_id in MessageTable.INVALID_FIELD_VALUES or new_message_content in MessageTable.INVALID_FIELD_VALUES:
            raise Exception("Error: A field value is empty.")
        
        elif message_id not in MessageTable.get_all_message_ids():
            raise Exception(f"Error: Message with message_id '{message_id}' does not exist.")
        
        elif len(new_message_content) > MessageTable.MAX_MESSAGE_LENGTH:
            raise Exception("Error: Message text is longer than 2000 chars.")
        
        else:
            parameter_dictionary = {
                'message_id': message_id,
                'new_message_content': new_message_content
            }
            query = """
            UPDATE database1.message
            SET message_content = :new_message_content
            WHERE message_id = :message_id;
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
    
    
    @staticmethod
    def delete_message(message_id):
        if message_id in MessageTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Message ID cannot be empty.")
        
        elif message_id not in MessageTable.get_all_message_ids():
            raise Exception(f"Error: Message with message_id '{message_id}' does not exist.")
        
        else:
            parameter_dictionary = {
                'message_id': message_id
            }
            query = """
            DELETE FROM database1.message
            WHERE message_id = :message_id;
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)



class InviteRequestTable:
    INVALID_FIELD_VALUES = [None, '']
    
    @staticmethod
    def get_number_of_invite_requests() -> int:
        """_summary_
        Returns number of invite requests in invite_request table
        
        Returns:
            int: number of invite requests in invite_request table
        """
        result = query_db("SELECT COUNT(request_id) FROM database1.invite_request;")
        return result[0][0]
    
    @staticmethod
    def get_number_received_invite_requests(receiver_username: str) -> int:
        """_summary_
        Get number of invite requests a user has received
        Args:
            receiver_username (str): the user who is receiving the invite requests

        Raises:
            Exception: receiver_username is empty
            Exception: receiver_username not in User Table (does not exist)

        Returns:
            int: number of invite requests specified user has received
        """
        
        if receiver_username in InviteRequestTable.INVALID_FIELD_VALUES:
            raise Exception("Error: A field value is empty.")
        
        elif receiver_username not in UserTable.get_all_usernames():
            raise Exception(f"Error: User '{receiver_username}' does not exist.")
        else:
            parameter_dictionary = {
            'receiver_username': receiver_username
            }        
            query = "SELECT COUNT(*) FROM database1.invite_request WHERE receiver_username = :receiver_username"
            return query_db(query, parameter_dictionary=parameter_dictionary)[0][0] 
        
    
    @staticmethod
    def check_invite_request_id_not_in_use(request_id: int) -> bool:
        """_summary_
        Checks if invite_request_id is not in use
        
        Args:
            request_id (int): primary key field of invite_request table
        
        Returns:
            bool: True if invite_request_id is not in use, False otherwise
        """
        parameter_dictionary = {
            'request_id': request_id
        }
        query = "SELECT COUNT(*) FROM database1.invite_request WHERE request_id = :request_id;"
        
        return query_db(query, parameter_dictionary=parameter_dictionary)[0][0] == 0
    
    
    # CREATE
    @staticmethod
    def create_invite_request(receiver_username: str, sender_username: str, group_id: int, status: str) -> None:
        """_summary_
        Creates an invite_request record in the invite_request table - calling context must specify receiver_username, sender_username, group_id, and status
        
        Args:
            receiver_username (str): username of user to receive invite
            sender_username (str): username of user who sent invite
            group_id (int): group_id of group invite is for
            status (str): status of invite request (pending, accepted, or rejected)
        
        Raises:
            Exception: receiver_username, sender_username, group_id, or status is empty
            Exception: receiver_username, sender_username, or group_id does not exist
            Exception: status is not one of 'pending', 'accepted', or 'rejected'
        
        Returns:
            None
        """
        if receiver_username in InviteRequestTable.INVALID_FIELD_VALUES or sender_username in InviteRequestTable.INVALID_FIELD_VALUES \
            or group_id in InviteRequestTable.INVALID_FIELD_VALUES or status in InviteRequestTable.INVALID_FIELD_VALUES:
            raise Exception("Error: A field value is empty.")
        
        elif receiver_username not in UserTable.get_all_usernames():
            raise Exception(f"Error: User '{receiver_username}' does not exist.")
        
        elif sender_username not in UserTable.get_all_usernames():
            raise Exception(f"Error: User '{sender_username}' does not exist.")
        
        elif UserTable.check_user_in_group(sender_username, group_id) == False:
            raise Exception(f"User {sender_username} not in group with group_id {group_id}. User must be in the group to invite others to it. ")            
        
        elif group_id not in GroupTable.get_all_group_ids():
            raise Exception(f"Error: Group '{group_id}' does not exist.")
        
        elif status not in ['pending', 'accepted', 'rejected']:
            raise Exception("Error: Invalid status. Status must be one of 'pending', 'accepted', or 'rejected'.")
        
        else:
            parameter_dictionary = {
                'receiver_username': receiver_username,
                'sender_username': sender_username,
                'group_id': group_id,
                'status': status
            }
            query = """
            INSERT INTO database1.invite_request (receiver_username, sender_username, group_id, status)
            VALUES (:receiver_username, :sender_username, :group_id, :status);
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
        
        
    # READ
    @staticmethod
    def get_invite_request_record_by_request_id(request_id: int) -> dict:
        """_summary_
        Returns dictionary of invite_request data for a given request_id
        
        Args:
            request_id (int): primary key field of invite_request table
        
        Raises:
            Exception: request_id cannot be empty
            Exception: request with request_id does not exist
        
        Returns:
            dict: dictionary of request_id, receiver_username, sender_username, group_id, status
        """
        if request_id in InviteRequestTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Request ID cannot be empty.")
        
        elif InviteRequestTable.check_invite_request_id_not_in_use(request_id):
            raise Exception(f"Error: Request with request_id '{request_id}' does not exist.")
        
        else:
            parameter_dictionary = {
                'request_id': request_id
            }
            raw_tuple_output = query_db("SELECT * FROM database1.invite_request WHERE request_id = :request_id;", \
                parameter_dictionary=parameter_dictionary)[0]
            
            dictionary_output = {
                'request_id': raw_tuple_output[0],
                'receiver_username': raw_tuple_output[1],
                'sender_username': raw_tuple_output[2],
                'group_id': raw_tuple_output[3],
                'status': raw_tuple_output[4]
            }
            return dictionary_output
        
    def get_received_invite_requests(receiver_username: str) -> list:
        
        """Gets list of received invite requests (as dictionaries) for a specific user.

        Args:
            receiver_username (str): The user who is receiving these invite requests

        Raises:
            Exception: receiver_username is empty
            Exception: receiver username does not exist (not in user table)

        Returns:
            list: list of dictionaries {sender_username, group_name, status, request_date_time}
        """        
        if receiver_username in InviteRequestTable.INVALID_FIELD_VALUES:
            raise Exception("Error: A field value is empty.")
        elif receiver_username not in UserTable.get_all_usernames():
            raise Exception(f"Error: User '{receiver_username}' does not exist.")
        else:
            parameter_dictionary = {
            'receiver_username': receiver_username
            }        
            query = """SELECT sender_username, group_name, status, request_date_time, request_id
                    FROM database1.invite_request, database1.group 
                    WHERE database1.invite_request.receiver_username = :receiver_username 
                    AND database1.group.group_id = database1.invite_request.group_id
                    ORDER BY
                        CASE
                            WHEN status = 'pending' THEN 1
                            ELSE 2
                        END,
                        request_date_time DESC;"""
            results =  query_db(query, parameter_dictionary=parameter_dictionary)
            
            invite_requests = []
            
            for result in results:
                                 
                invite_requests.append({
                    "sender_username": result[0],
                    "group_name": result[1],
                    "status": result[2],
                    "request_date_time": result[3],
                    "request_id": result[4],
                    
                })
            return invite_requests 
        
    
    def get_sent_invite_requests(sender_username: str) -> list:
        """Gets list of sent invite requests (as dictionaries) for a specific user.

        Args:
            sender_username (str): User who has sent these invite requests.

        Raises:
            Exception: sender_username is empty
            Exception: user with sender_username does not exist (not in user table)

        Returns:
            list: list of dictionaries of invite requests (receiver_username, group_name, status, request_date_time)
        """
        if sender_username in InviteRequestTable.INVALID_FIELD_VALUES:
            raise Exception("Error: A field value is empty.")
        elif sender_username not in UserTable.get_all_usernames():
            raise Exception(f"Error: User '{sender_username}' does not exist.")
        else:
            parameter_dictionary = {
            'sender_username': sender_username
            }        
            query = """SELECT receiver_username, group_name, status, request_date_time, request_id
                    FROM database1.invite_request, database1.group 
                    WHERE database1.invite_request.sender_username = :sender_username 
                    AND database1.group.group_id = database1.invite_request.group_id
                    ORDER BY
                        CASE
                            WHEN status = 'pending' THEN 1
                            ELSE 2
                        END,
                        request_date_time DESC;"""
            results =  query_db(query, parameter_dictionary=parameter_dictionary)
            
            invite_requests = []
            
            for result in results:
                                 
                invite_requests.append({
                    "receiver_username": result[0],
                    "group_name": result[1],
                    "status": result[2],
                    "request_date_time": result[3],
                    "request_id": result[4],
                    
                })
            return invite_requests
        
        
    # UPDATE
    @staticmethod
    def update_invite_request_status(request_id: int, new_status: str) -> None:
        """_summary_
        Updates status field in invite_request table for a given request_id
        
        Args:
            request_id (int): primary key field of invite_request table
            new_status (str): new status to update request with
        
        Raises:
            Exception: request_id or new_status is empty
            Exception: status is not one of 'pending', 'accepted', or 'rejected'
            Exception: status has not changed
            Exception: request with request_id does not exist
        
        Returns:
            None
        """
        if request_id in InviteRequestTable.INVALID_FIELD_VALUES or new_status in InviteRequestTable.INVALID_FIELD_VALUES:
            raise Exception("Error: A field value is empty.")
        
        elif new_status not in ['pending', 'accepted', 'rejected']:
            raise Exception("Error: Invalid status. Status must be one of 'pending', 'accepted', or 'rejected'.")
        
        elif InviteRequestTable.check_invite_request_id_not_in_use(request_id):
            raise Exception(f"Error: Request with request_id '{request_id}' does not exist.")
        
        elif new_status == InviteRequestTable.get_invite_request_record_by_request_id(request_id)['status']:
            raise Exception("Error: Status has not changed.")
        
        else:
            parameter_dictionary = {
                'request_id': request_id,
                'new_status': new_status
            }
            query = """
            UPDATE database1.invite_request
            SET status = :new_status
            WHERE request_id = :request_id;
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
        
        
    # DELETE
    @staticmethod
    def delete_invite_request(request_id: int) -> None:
        """_summary_
        Deletes an invite_request record in the invite_request table - calling context must specify request_id
        
        Args:
            request_id (int): primary key field of invite_request table
        
        Raises:
            Exception: request_id cannot be empty
            Exception: request with request_id does not exist
        
        Returns:
            None
        """
        if request_id in InviteRequestTable.INVALID_FIELD_VALUES:
            raise Exception("Error: Request ID cannot be empty.")
        
        elif InviteRequestTable.check_invite_request_id_not_in_use(request_id):
            raise Exception(f"Error: Request with request_id '{request_id}' does not exist.")
        
        else:
            parameter_dictionary = {
                'request_id': request_id
            }
            query = """
            DELETE FROM database1.invite_request
            WHERE request_id = :request_id;
            """
            return query_db(query, parameter_dictionary=parameter_dictionary, no_return=True)
        
if __name__ == "__main__":
    #print(UserTable.check_user_in_group("avinash255", 7))
    #print(GroupTable.get_number_of_users(5))
    #print(GroupTable.get_number_of_online_users(5))
    
    #print(UserTable.get_pending_invite_requests("avingo255"))
    #print(GroupTable.get_group_user_details(5))
    pass
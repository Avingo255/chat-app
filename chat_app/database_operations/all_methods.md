# Classes, Methods, Attributes, and Docstrings

## Class: UserTable
### Attributes:
- INVALID_FIELD_VALUES = [None, '']

### Methods:
- `get_number_of_users() -> int`
  - **Docstring:**
    ```python
    """_summary_
    Returns number of users in user table
    
    Returns:
        int: number of users in user table
    """
    ```

- [check_username_exists(username: str) -> bool](http://_vscodecontentref_/0)
  - **Docstring:**
    ```python
    """_summary_
    Checks if username exists in user table
    
    Args:
        username (str): username to check
        
    Returns:
        bool: True if username exists, False otherwise
    """
    ```

- [validate_password(raw_password: str) -> list](http://_vscodecontentref_/1)
  - **Docstring:**
    ```python
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
    ```

- [check_form_group_valid(form_group: str) -> bool](http://_vscodecontentref_/2)
  - **Docstring:**
    ```python
    """_summary_
    Checks if form_group is valid
    
    Args:
        form_group (str): form_group to check
    
    Returns:
        bool: True if form_group is valid, False otherwise
    """
    ```

- [create_user(username: str, display_name: str, form_group: str, raw_password: str) -> None](http://_vscodecontentref_/3)
  - **Docstring:**
    ```python
    """_summary_
    Creates a user in the user table - calling context must specify username, display_name, form_group, and raw_password
    
    Args:
        username (str): username (PK) of user
        display_name (str): display name of user
        form_group (str): form_group of user, must meet criteria specified by UserTable.check_form_group_valid
        raw_password (str): raw password of user, must meet criteria specified by UserTable.validate_password
    
    Raises:
        Exception: username, display_name, form_group, or raw_password is empty
        Exception: form_group is invalid
        Exception: password is invalid
        Exception: username already exists
    
    Returns:
        None
    """
    ```

- [get_user_record_by_username(username: str) -> dict](http://_vscodecontentref_/4)
  - **Docstring:**
    ```python
    """_summary_
    Returns dictionary of user data for a given username
    
    Args:
        username (str): username (PK) of record in User table to be accessedd
    
    Raises:
        Exception: username is empty
        Exception: username not in table

    Returns:
        dict: dictionary of user data (username, display_name, form_group, datetime_joined, password_hash, is_authenticated, is_active, is_anonymous)
    """
    ```

- [check_user_in_group(username: str, group_id: int) -> bool](http://_vscodecontentref_/5)
  - **Docstring:**
    ```python
    """_summary_
    Checks if user with username is in group with group_id
    
    Args:
        username (str): username (PK) of user
        group_id (int): group_id (PK) of group
    
    Returns:
        bool: True if user is in group, False otherwise
    """
    ```

- [get_number_user_groups(username: str) -> int](http://_vscodecontentref_/6)
  - **Docstring:**
    ```python
    """_summary_
    Returns number of groups user is in
    
    Args:
        username (str): username (PK) of user to get number of groups for
    
    Raises:
        Exception: username is empty
        Exception: username not in table

    Returns:
        int: number of groups user is in
    """
    ```

- [get_user_groups(username: str) -> dict](http://_vscodecontentref_/7)
  - **Docstring:**
    ```python
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
    ```

- [get_pending_invite_requests(username: str) -> list](http://_vscodecontentref_/8)
  - **Docstring:**
    ```python
    """_summary_
    Returns list of tuples of pending invite request records for a given username
    
    Args:
        username (str): username (PK) of user to get pending invite requests for
    
    Raises:
        Exception: username is empty
        Exception: username not in table
    
    Returns:
        list: list of all pending invite request records for specified username"""
    ```

- [update_existing_user_field(username: str, field: str, new_value: str) -> None](http://_vscodecontentref_/9)
  - string**Doc:**
    ```python
    """field can be 'username', 'display_name', 'form_group', 'password_hash', 'is_authenticated', 'is_active'
    if field to update is 'password_hash', new_value can be raw password
    cannot update 'datetime_joined' or 'is_anonymous' fields
    Note: even if new_value is a boolean, it must be passed as a string for the sql query to work"""
    
    """_summary_
    Updates a field in the user table for a given username
    
    Args:
        username (str): username (PK) of user to update
        field (str): field to update, must be one of: [username, display_name, form_group, password_hash, is_authenticated, is_active]
        new_value (str): new value to update field with
        
    Raises: 
        Exception: field is invalid
        Exception: new_value is empty
        Exception: form_group is invalid
        Exception: username already exists
        Exception: display_name has not changed
    
    Returns:
        None
    """
    ```

- [delete_user(username: str) -> None](http://_vscodecontentref_/10)
  - **Docstring:**
    ```python
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
    ```

## Class: GroupTable
### Attributes:
- INVALID_FIELD_VALUES = [None, '']

### Methods:
- [check_group_exists(group_id: int) -> bool](http://_vscodecontentref_/11)
  - **Docstring:**
    ```python
    """_summary_
    Checks if group with group_id exists
        
    Args:
        group_id (int): primary key field of group table
        
    Returns:
        bool: True if group exists, False otherwise
    """
    ```

- [get_number_of_groups() -> int](http://_vscodecontentref_/12)
  - **Docstring:**
    ```python
    """Returns number of groups in group table"""
    ```

- [get_last_group_id()](http://_vscodecontentref_/13)
  - **Docstring:**
    ```python
    """_summary_
    Returns the last group_id that was created
    
    Returns:
        int: last group_id that was created
    """
    ```

- [create_group(group_name: str) -> None](http://_vscodecontentref_/14)
  - **Docstring:**
    ```python
    """_summary_
    Creates a group in the group table - calling context must specify group_name
    
    Args:
        group_name (str): name of group to create
        
    Raises:
        Exception: group_name is empty
    
    Returns:
        None
    """
    ```

- [get_group_record_by_group_id(group_id: int) -> dict](http://_vscodecontentref_/15)
  - **Docstring:**
    ```python
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
    ```

- [get_number_of_users(group_id: int) -> int](http://_vscodecontentref_/16)
  - **Docstring:**
    ```python
    """Returns number of users in a given group"""
    ```

- [get_number_of_online_users(group_id: int) -> int](http://_vscodecontentref_/17)
  - **Docstring:**
    ```python
    """Returns number of online users in a given group"""
    ```

- [get_group_users(group_id: int) -> list](http://_vscodecontentref_/18)
  - **Docstring:**
    ```python
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
    ```

- [get_group_user_details(group_id: int) -> dict](http://_vscodecontentref_/19)
  - **Docstring:**
    ```python
    """_summary_
    Returns dictionary of username, user display name, form group,  is_authenticated for every user in the group

    Args:
        group_id (int): primary key field of group table

    Raises:
        Exception: group_id cannot be empty
        Exception: group with group_id does not exist

    Returns:
        dict: dictionary of username, user display name, form group, is_authenticated for every user in the group
    """
    ```

- [get_group_datetime_created(group_id: int) -> str](http://_vscodecontentref_/20)
  - **Docstring:**
    ```python
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
    ```

- [get_all_group_messages(group_id: int) -> list](http://_vscodecontentref_/21)
  - **Docstring:**
    ```python
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
    ```

- [get_latest_group_message(group_id: int) -> tuple](http://_vscodecontentref_/22)
  - **Docstring:**
    ```python
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
    ```

- [update_group_name(group_id: int, new_group_name: str) -> None](http://_vscodecontentref_/23)
  - **Docstring:**
    ```python
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
    ```

- [delete_group(group_id: int) -> None](http://_vscodecontentref_/24)
  - **Docstring:**
    ```python
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
    ```

## Class: UserGroupTable
### Attributes:
- INVALID_FIELD_VALUES = [None, '']

### Methods:
- [create_user_group(username: str, group_id: int) -> None](http://_vscodecontentref_/25)
  - **Docstring:**
    ```python
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
    ```

- [delete_user_group(username, group_id)](http://_vscodecontentref_/26)
  - **Docstring:**
    ```python
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
    ```

## Class: MessageTable
### Attributes:
- INVALID_FIELD_VALUES = [None, '']
- MAX_MESSAGE_LENGTH = 2000

### Methods:
- [check_message_exists(message_id: int) -> bool](http://_vscodecontentref_/27)
  - **Docstring:**
    ```python
    """_summary_
    Checks if message with message_id exists
    
    Args:
        message_id (int): primary key field of message table
    
    Returns:
        bool: True if message exists, False otherwise
    """
    ```

- [get_number_of_messages() -> int](http://_vscodecontentref_/28)
  - **Docstring:**
    ```python
    """_summary_
    Returns number of messages in message table
    Returns:
        int: number of messages in message table
    """
    ```

- [create_message(message_content: str, sender_username: str, group_id: int) -> None](http://_vscodecontentref_/29)
  - **Docstring:**
    ```python
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
    ```

- [get_message_record_by_message_id(message_id: int) -> dict](http://_vscodecontentref_/30)
  - **Docstring:**
    ```python
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
    ```

- [update_message_content(message_id: int, new_message_content)](http://_vscodecontentref_/31)
  - **Docstring:**
    ```python
    """_summary_
    Updates message content for a given message_id
    
    Args:
        message_id (int): primary key field of message table
        new_message_content (str): new content to update message with
    
    Raises:
        Exception: message_id or new_message_content is empty
        Exception: message with message_id does not exist
        Exception: new_message_content length is > MessageTable.MAX_MESSAGE_LENGTH (2000) characters
    
    Returns:
        None
    """
    ```

- [delete_message(message_id)](http://_vscodecontentref_/32)
  - **Docstring:**
    ```python
    """_summary_
    Deletes a message from the message table with a given message_id
    
    Args:
        message_id (int): primary key field of message table
    
    Raises:
        Exception: message_id is empty
        Exception: message with message_id does not exist
    
    Returns:
        None
    """
    ```
## Class: InviteRequestTable
### Attributes:
- INVALID_FIELD_VALUES = [None, '']

### Methods:
- `get_number_of_invite_requests() -> int`
  - **Docstring:**
    ```python
    """_summary_
    Returns number of invite requests in invite_request table
    
    Returns:
        int: number of invite requests in invite_request table
    """
    ```

- `get_number_received_invite_requests(receiver_username: str) -> int`
  - **Docstring:**
    ```python
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
    ```

- `check_invite_request_id_not_in_use(request_id: int) -> bool`
  - **Docstring:**
    ```python
    """_summary_
    Checks if invite_request_id is not in use
    
    Args:
        request_id (int): primary key field of invite_request table
    
    Returns:
        bool: True if invite_request_id is not in use, False otherwise
    """
    ```

- `create_invite_request(receiver_username: str, sender_username: str, group_id: int, status: str) -> None`
  - **Docstring:**
    ```python
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
    ```

- `get_invite_request_record_by_request_id(request_id: int) -> dict`
  - **Docstring:**
    ```python
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
    ```

- `get_received_invite_requests(receiver_username: str) -> list`
  - **Docstring:**
    ```python
    """Gets list of received invite requests (as dictionaries) for a specific user.

    Args:
        receiver_username (str): The user who is receiving these invite requests

    Raises:
        Exception: receiver_username is empty
        Exception: receiver username does not exist (not in user table)

    Returns:
        list: list of dictionaries {sender_username, group_name, status, request_date_time}
    """
    ```

- `get_sent_invite_requests(sender_username: str) -> list`
  - **Docstring:**
    ```python
    """Gets list of sent invite requests (as dictionaries) for a specific user.

    Args:
        sender_username (str): User who has sent these invite requests.

    Raises:
        Exception: sender_username is empty
        Exception: user with sender_username does not exist (not in user table)

    Returns:
        list: list of dictionaries of invite requests (receiver_username, group_name, status, request_date_time)
    """
    ```

- `update_invite_request_status(request_id: int, new_status: str) -> None`
  - **Docstring:**
    ```python
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
    ```

- `delete_invite_request(request_id: int) -> None`
  - **Docstring:**
    ```python
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
    ```
from chat_app import app
from flask import render_template, flash, redirect, url_for, request, jsonify, make_response, abort
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

from chat_app.database_operations.models import UserTable, GroupTable, UserGroupTable, MessageTable, InviteRequestTable
from werkzeug.security import check_password_hash
from chat_app.auth import User

from chat_app.forms import SignInForm, SignUpForm, BubbleForm

import re

#validation function that returns True if string only has alphanumeric characters or spaces, false otherwise
def is_alphanumeric_or_space(string: str) -> bool:
    """_summary_
    Checks if a string contains only alphanumeric characters or spaces.
    
    Args:
        string (str): The string to check.
        
    Returns:
        bool: True if the string contains only alphanumeric characters or spaces, False otherwise.
    """
    return bool(re.match(r'^[a-zA-Z0-9 ]*$', string))
    

#used for extracting group_id from URL - used in leave_group() function
def extract_group_id(url: str) -> int:
    """_summary_    
    Extracts the group ID from a given URL.
    
    Args:
        url (str): The URL string from which to extract the group ID.
    
    Returns:
        int: The extracted group ID if the URL matches the expected pattern, otherwise None.
    """

    # Regex pattern to match the URL format
    pattern = r'/chat/(\d+)(?:/options)?$'
    
    # Detailed explanation of the regex pattern:
    # /chat/   : Matches the literal string "/chat/"
    # (        : Start of capturing group
    #   \d+    : Matches one or more digits (0-9)
    # )        : End of capturing group
    # (?:      : Start of non-capturing group
    #   /options : Matches the literal string "/options"
    # )?       : End of non-capturing group, ? makes this group optional
    # $        : Asserts position at the end of the string
    
    # Search for the pattern in the URL
    match = re.search(pattern, url)
    
    if match:
        # Extract the group_id and convert to int
        group_id = int(match.group(1))
        return group_id
    else:
        # Return None if no match is found
        return None

#
# APIS
#

#route to remove current_user from a group
@app.route('/leave-group', methods = ['POST'])
def leave_group():
    """
    Allows the current authenticated user to leave a group.
        If the user is not authenticated, a 403 error is raised - user is redirected to a 403 page - there is a separate route for this.
    
    If the group ID extracted from the request parameters is invalid, an error message is flashed.
    
    If the user is not a member of the group, a 403 error is raised.
    Will use UserTable.check_user_in_group() to check if the user is in the group.
    
    If the user successfully leaves the group, a success message is flashed.
    UserTable.delete_user_group() is used to remove the user from the group.
    
    This API is slightly different from the others in that it is not called by the JavaScript, but is instead called when the user clicks the 'Leave Group' button on a group options panel.
    
    Returns:
        A redirect response to the index page.
    """
    
    if current_user.is_authenticated == False:
        abort(403)
    else:
        print('HELLO')
        print(extract_group_id(request.referrer))
        group_id = extract_group_id(request.referrer)
        
        if group_id == None:
            flash('Error: Invalid group ID')
        elif UserTable.check_user_in_group(current_user.username, group_id) == False:
            abort(403)
        else:
            UserGroupTable.delete_user_group(current_user.username, group_id)
            flash('You have left the group, never to return.')
        return redirect(url_for('index'))

#route to get number of online users in a group
@app.route('/number-online-users', methods = ['POST'])
def number_online_users():
    """
    Get the number of online users in a specific group.
    
    This function checks if the current user is authenticated. If not, it returns a response indicating that the user is unauthenticated. This uses flask_login's session cookie functionality.
    
    If the user is authenticated, it retrieves the group ID from the request JSON parameters, fetches the number of online users using GroupTable.get_number_of_online_users(),
    and returns the count in a JSON response.
    Returns:
        Response: A JSON response containing either the number of online users or an error message with the appropriate HTTP status code.
    """
    
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else: 
        group_id = int(request.json['group_id'])
        number_online_users = GroupTable.get_number_of_online_users(group_id)
        return make_response(jsonify(number_online_users), 200)

@app.route('/number-total-users', methods = ['POST'])
def number_total_users():
    """
    Get the total number of users in a group.
    
    This function checks if the current user is authenticated. This uses flask_login's session cookie functionality.
    If not, it returns a response indicating that the user is unauthenticated, with a 401 code.
    
    If the user is authenticated, it retrieves the group ID from the request JSON parameters, fetches the total number of users in the specified group,
    and returns this number in the response. This uses GroupTable.get_number_of_users().

    Returns:
        Response: A JSON response containing either an error message with a 401 status code if the user is unauthenticated,
                  or the total number of users in the group with a 200 status code.
    """
    
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else: 
        group_id = int(request.json['group_id'])
        number_total_users = GroupTable.get_number_of_users(group_id)
        return make_response(jsonify(number_total_users), 200)

@app.route('/group-list', methods = ['POST']) 
def group_list():
    """
    Retrieve the list of groups for the authenticated user.
    
    If the current user is not authenticated (this uses flask_login's session cookie functionality), returns a 401 response with an 'UNAUTHENTICATED USER' message.
    
    Otherwise, retrieves the list of groups associated with the current user's username from the UserTable
    and returns it in a 200 response.
    
    This uses UserTable.get_user_groups() to retrieve the list of groups for the current user (this uses that same flask_login session cookie functionality).
    
    Returns:
        Response: A Flask response object containing the list of user groups in JSON format with a 200 status code,
                  or an 'UNAUTHENTICATED USER' message with a 401 status code if the user is not authenticated.
    """

    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        user_group_list = UserTable.get_user_groups(current_user.username)
        
        return make_response(jsonify(user_group_list), 200)
    
@app.route('/group-user-details', methods = ['POST'])
def group_user_details():
    """
    Retrieve details of users in a specified group.
    
    This function checks if the current user is authenticated. If not, it returns a 401 response indicating an unauthenticated user.
    This uses flask_login's session cookie functionality.
    
    If the user is authenticated, it retrieves the group ID from the request JSON parameters, fetches the user details for that group
    from the GroupTable using GroupTable.get_user_group_details(), and returns the details as a JSON response.
    Returns:
        Response: A JSON response containing either an error message with a 401 status code if the user is unauthenticated,
                  or a list of user details with a 200 status code if the user is authenticated.
    """
    
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        group_id = int(request.json['group_id'])
        user_list = GroupTable.get_group_user_details(group_id)
        #list of dictionaries {username, display_name, is_authenticated}
        
        return make_response(jsonify(user_list), 200)


@app.route('/all-group-messages', methods = ['POST'])
def all_group_messages():
    """
    Retrieve all messages for a specific group.
    
    This function checks if the current user is authenticated. If not, it returns a 401 response.
    This will prevent unauthorised access of data and uses flask_login's session cookie functionality.
    
    If authenticated, it retrieves all messages for the specified group ID from the request JSON parameters.
    The messages are then formatted into a response list with additional user information.
    Returns:
        Response: A JSON response containing a list of messages with the following fields:
            - message_id (int): The ID of the message.
            - message_content (str): The content of the message.
            - message_date_time (str): The date and time the message was sent, formatted as '%d/%m/%y %H:%M:%S' using strftime.
            - sender_username (str): The username of the sender.
            - sender_display_name (str): The display name of the sender.
            - usertype (str): Indicates if the sender is the current user ('current-user') or another user ('other-user').
    Raises:
        401 Error: If user is not authenticated. This will prevent unauthorised access of data. This will redirect the user to a 401 error page.
    """
    
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        group_id = int(request.json['group_id'])
        
        messages = GroupTable.get_all_group_messages(group_id)
        #tuple format: (message_id, message_content, message_date_time, sender_username, sender_display_name)
        response = []
        for message in messages:
            if message[3] == current_user.username:
                usertype = 'current-user'
                sender_display_name = 'You'
            else:
                usertype = 'other-user'
                sender_display_name = message[4]

            
            response.append({
                'message_id': message[0],
                'message_content': message[1],
                'message_date_time': message[2].strftime('%d/%m/%y %H:%M:%S'),
                'sender_username': message[3], 
                'sender_display_name': sender_display_name,
                'usertype': usertype
            })
            
        return make_response(jsonify(response), 200)


@app.route('/latest-group-message', methods = ['POST'])
def latest_group_message():
    """
    Retrieve the latest message from a group chat.
    This function checks if the current user is authenticated. If not, it returns a 401 response. This will redirect the user to a 401 error page.
    If authenticated, it retrieves the latest message from the specified group and formats the response.
    Returns:
        Response: A JSON response containing the latest message details or an error message if the user is unauthenticated.
    
    Response JSON Structure:
        {
            'message_id': int,
            'message_content': str,
            'message_date_time': str (formatted as '%d/%m/%y %H:%M:%S'),
            'sender_username': str,
            'sender_display_name': str,
            'usertype': str ('current-user' or 'other-user')
    """
    
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        group_id = int(request.json['group_id'])
        
        message = GroupTable.get_latest_group_message(group_id)[0]
        #tuple format: (message_id, message_content, message_date_time, sender_username, sender_display_name)
        
        if message[3] == current_user.username:
            usertype = 'current-user'
            sender_display_name = 'You'
        else:
            usertype = 'other-user'
            sender_display_name = message[4]
        
        response = {
            'message_id': message[0],
            'message_content': message[1],
            'message_date_time': message[2].strftime('%d/%m/%y %H:%M:%S'),
            'sender_username': message[3], 
            'sender_display_name': sender_display_name,
            'usertype': usertype
        }
        
        return make_response(jsonify(response), 200)


@app.route('/send-message', methods = ['POST'])
def send_message():
    """
    Handles the sending of a message by an authenticated user.
    Returns:
        Response: A JSON response indicating the result of the message sending operation.
                  - If the message is successfully sent, returns a 200 status with 'MESSAGE SENT'.
    Raises:
        401 Error: If user is not authenticated. This will prevent unauthorised access of data.
    """
    
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        message_content = request.json['message_content']
        group_id = int(request.json['group'])
        sender_username = current_user.username
        
        MessageTable.create_message(message_content, sender_username, group_id)
        
        return make_response(jsonify('MESSAGE SENT'), 200)
    
    
    
@app.route('/all-received-group-invites', methods = ['POST'])
def all_received_group_invites():
    """
    Retrieve all received group invites for the authenticated user.
    This function checks if the current user is authenticated. If not, it returns a 401 UNAUTHENTICATED USER response.
    If the user is authenticated, it fetches all received group invites from the InviteRequestTable.get_received_invite_requests() for the current user.
    The invites are then formatted into a list of dictionaries containing the sender's username, group name, request date and time,
    status, and request ID. The formatted list is returned as a JSON response with a 200 status code.
    Returns:
        Response: A JSON response containing a list of dictionaries with the following keys:
            - sender_username (str): The username of the sender.
            - group_name (str): The name of the group.
            - request_date_time (str): The date and time of the request in the format '%d/%m/%y %H:%M:%S'.
            - status (str): The status of the invite.
            - request_id (int): The ID of the request.
    
    Raises:
        401 Error: If user is not authenticated. This will prevent unauthorised access of data.
    """
    
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        all_received_group_invites = InviteRequestTable.get_received_invite_requests(current_user.username)
        #list of dictionaries {sender_username, group_name, status, request_date_time, request_id}
        response = []
        for invite in all_received_group_invites:
            response.append({
                'sender_username': invite['sender_username'],
                'group_name': invite['group_name'],
                #'request_date_time': invite['request_date_time'].strftime('%d/%m/%y'),
                'request_date_time': invite['request_date_time'].strftime('%d/%m/%y %H:%M:%S'), # with h:m:s time as well
                'status': invite['status'],
                'request_id': invite['request_id'], 
            })
        
        return make_response(jsonify(response), 200)

@app.route('/all-sent-group-invites', methods = ['POST'])
def all_sent_group_invites():
    
    """
    Retrieve all group invites sent by the current authenticated user.
    This function checks if the current user is authenticated. If not, it returns a 401 response indicating an unauthenticated user.
    If the user is authenticated, it fetches all sent group invite requests from the InviteRequestTable.get_sent_invite_requests() for the current user's username.
    The invite requests are then formatted into a list of dictionaries containing the receiver's username, group name, request date and time,
    status, and request ID. The formatted list is returned as a JSON response with a 200 status code.
    Returns:
        Response: A Flask response object containing a JSON list of sent group invites and a status code.
    Raises:
        401 error: If the user is not authenticated.
    
    """
    
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        all_received_group_invites = InviteRequestTable.get_sent_invite_requests(current_user.username)
        #list of dictionaries {receiver_username, group_name, status, request_date_time, request_id}
        
        response = []
        for invite in all_received_group_invites:
            response.append({
                'receiver_username': invite['receiver_username'],
                'group_name': invite['group_name'],
                'request_date_time': invite['request_date_time'].strftime('%d/%m/%y %H:%M:%S'),
                'status': invite['status'],
                'request_id': invite['request_id'],  
            })
        
        return make_response(jsonify(response), 200)

@app.route('/accept-invite', methods = ['POST'])
def accept_invite():
    """
    Accepts an invite request for the current authenticated user.
    Returns:
        Response: A JSON response indicating the result of the operation.
            - 200 if the invite request is successfully accepted.
    Raises:
        401 Error: If user is not authenticated.
    """
    
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        request_id = request.json['request_id']
        
        #update status
        InviteRequestTable.update_invite_request_status(request_id, "accepted")
        
        #add user to group
        group_id = InviteRequestTable.get_invite_request_record_by_request_id(request_id)['group_id']
        UserGroupTable.create_user_group(current_user.username, group_id)
        return make_response(jsonify('INVITE REQUEST ACCEPTED'), 200)


@app.route('/reject-invite', methods = ['POST'])
def reject_invite():
    """
    Rejects an invite request.
    This function checks if the current user is authenticated. If not, it returns a 401 response.
    If the user is authenticated, it retrieves the request ID from the JSON payload of the request,
    updates the invite request status to "rejected" in the InviteRequestTable, and returns a 200 response.
    Returns:
        Response: A Flask response object with a JSON message and an appropriate HTTP status code.
    Raises:
        401 Error: If user is not authenticated. This will prevent unauthorised access to user data.
    """
    
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        request_id = request.json['request_id']
        
        #update status
        InviteRequestTable.update_invite_request_status(request_id, "rejected")
        
        return make_response(jsonify('INVITE REQUEST REJECTED'), 200)


@app.route('/cancel-outgoing-invite', methods = ['POST'])
def cancel_outgoing_invite():
    """
    Cancels an outgoing invite request.
    This function checks if the current user is authenticated. If not, it returns a 401 response indicating an unauthenticated user.
    If the user is authenticated, it retrieves the request ID from the JSON payload of the request, deletes the invite request from the 
    InviteRequestTable using InviteRequest.delete_invite_request(), and returns a 200 response indicating that the invite request has been cancelled.
    Returns:
        Response: A Flask response object with a JSON message and an appropriate HTTP status code - 200.
    Raises:
        401 Error: If user is not authenticated. This will prevent unauthorised access to user data.
    """
    
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        request_id = request.json['request_id']
        
        #update status
        InviteRequestTable.delete_invite_request(request_id)
        
        return make_response(jsonify('INVITE REQUEST CANCELLED'), 200)


# ------------------------------------------------------------------- #
#                                                                     #                            
#                                                                     #
#                           ACTUAL WEBPAGE                            #
#                               ROUTES                                #  
#                                                                     #  
#                                                                     #  
# ------------------------------------------------------------------- #

@app.route('/')
@app.route('/index')
def index():
    """
    Render the index page for the chat application.
    If the current user is authenticated, it checks if the user is part of any groups.
    If the user is not in any groups, it sets a placeholder message prompting the user
    to create a group or check group invites. If the user is in groups, it sets a 
    placeholder message to select a group chat.
    
    Note that the index page itself, will extend (template rendering is handled using the Jinja template engine) from group_list.html, which extends from base.html.
    This means that the template will render base.html, which will then render group_list.html within that.
    Index.html will then be rendered within group.html - this significantly reduces code repetition across templates.
    
    
    Returns:
        rendered template: Rendered template for the index page with the appropriate placeholder message
             if the user is authenticated.
        Response: Alternatively, redirect to the sign-in page if the user is not authenticated.
    """
    
    if current_user.is_authenticated:
        if UserTable.get_user_groups(current_user.username) == []:
            placeholder_message = "You are not in any groups. Click on 'Create Group' or check 'Group Invites' to end your solitude."
        else:
            placeholder_message = "Select a group chat to continue."
        return render_template('index.html', title=f'{current_user.display_name}\'s chats', placeholder_message=placeholder_message)
    else:
        return redirect(url_for('sign_in'))


@app.route('/chat/<group_id>')
@login_required
def chat_window(group_id):
    """
    Renders the chat window for a given group.
    This function is annotated with @login_required, which ensures that the user is authenticated before accessing the chat window.
    Users will be redirected to the sign-in page if they attempt to visit this page without being authenticated by Flask.
    Args:
        group_id (int or str): The ID of the group.
    Returns:
        Response: The rendered template for the chat window.
    Raises:
        404: If the group does not exist.
        403: If the current user is not a member of the group.
    """
    
    group_id = int(group_id)
    if GroupTable.check_group_exists(group_id) == False:
        abort(404)
    elif UserTable.check_user_in_group(current_user.username, group_id) == False:
        abort(403)
    else:    
        group_display_name = GroupTable.get_group_record_by_group_id(group_id)['group_name']
        number_online_users = GroupTable.get_number_of_online_users(group_id)
        number_users = GroupTable.get_number_of_users(group_id)
    
        return render_template('chat.html', group_display_name=group_display_name, group_id=str(group_id),  title=group_display_name, number_online_users=number_online_users, number_users=number_users)
    
@app.route('/chat/<group_id>/options')
@login_required
def chat_options(group_id):
    """
    Renders the chat options page for a given group.
    Args:
        group_id (int or str): The ID of the group.
    Returns:
        Response: The rendered template for the chat options page.
    Raises:
        404: If the group does not exist.
        403: If the current user is not a member of the group.
    """
    
    group_id = int(group_id)
    if GroupTable.check_group_exists(group_id) == False:
        abort(404)
    elif UserTable.check_user_in_group(current_user.username, group_id) == False:
        abort(403)
    else:
        group_display_name = GroupTable.get_group_record_by_group_id(group_id)['group_name']
        number_online_users = GroupTable.get_number_of_online_users(group_id)
        number_users = GroupTable.get_number_of_users(group_id)
        datetime_created = GroupTable.get_group_datetime_created(group_id)
        
        return render_template('chat_options.html', group_display_name=group_display_name, group_id=str(group_id), title=f"{group_display_name} | Options", number_online_users=number_online_users, number_users=number_users, datetime_created=datetime_created)    

@app.route('/group-invites')
@login_required
def group_invites():
    """
    Render the group invites page.
    This function checks the number of received invite requests for the current user.
    If there are no invite requests, it updates the subtitle to indicate that the user
    might be feeling lonely. It then renders the 'invites.html' template with the 
    appropriate title and subtitle.
    Returns:
        rendered template: The rendered HTML content for the group invites page.
    """
    
    subtitle = "Manage group invites here."
    if InviteRequestTable.get_number_received_invite_requests(current_user.username) == 0:
        subtitle = "Feeling lonely?"
    return render_template('invites.html', title="Group Invites", subtitle=subtitle)

@app.route('/create-group', methods=['GET', 'POST'])
def create_group():
    """
    Handle the creation of a new chat group.
    This function performs the following steps:
    1. Checks if the current user is authenticated. If not, redirects to the sign-in page.
    2. If authenticated, initializes the BubbleForm.
    3. Validates the form submission.
    4. Checks if the usernames in the bubble list are valid.
    5. Checks if the group name is valid (alphanumeric characters or spaces only).
    6. Creates a new group and adds the current user to the group.
    7. Sends invite requests to the users in the bubble list.
    Returns:
        - Redirects to the sign-in page if the user is not authenticated.
        - Renders the 'create_group.html' template with the form if there are validation errors.
        - Redirects to the chat window of the newly created group if successful.
    """
    
    if current_user.is_authenticated == False:
        return redirect(url_for('sign_in'))
    else:
        form = BubbleForm()
        if form.validate_on_submit():
            bubble_list = form.bubble_list.data
            group_name = form.group_name.data
            
            
            # 1. check usernames are valid
            invalid_usernames = []
            for username in bubble_list:
                if not username.isalnum() or UserTable.check_username_exists(username) == False:
                    
                    invalid_usernames.append(username)
                    
            # has the user tried to add themselves?
            if current_user.username in bubble_list:
                flash("You cannot add yourself to the group here - we will obviously add you to the group you have created.")
                return render_template('create_group.html', form=form)
            
            elif len(invalid_usernames) > 0:
                print(invalid_usernames)
                flash(f"Sadly, these users don't exist. Check your spelling. \n {invalid_usernames}")
                return render_template('create_group.html', form=form)
            elif len(bubble_list) == 0:
                flash("Please add at least one user to the group...")
                return render_template('create_group.html', form=form)
            else:
                GroupTable.create_group(group_name)
                group_id = GroupTable.get_last_group_id()
                UserGroupTable.create_user_group(current_user.username, group_id)
                
                for username in bubble_list:
                    InviteRequestTable.create_invite_request(username, current_user.username, group_id, 'pending')
                return redirect(url_for('chat_window', group_id=group_id))
                
        return render_template('create_group.html', form=form, title='Create Group')
    
    
@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    """
    Handle the sign-in process for users.
    If the current user is already authenticated, they are redirected to the index page.
    Otherwise, a sign-in form is presented to the user. Upon form submission, the user's
    credentials are validated. If the credentials are correct, the user is logged in and
    redirected to the next page or the index page. If the credentials are incorrect, an
    error message is flashed and the user is redirected back to the sign-in page.
    Returns:
        Response: A redirect response to the appropriate page based on the authentication
        status and form submission outcome.
    """
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignInForm()
    
    if form.validate_on_submit():
        try:
            user = UserTable.get_user_record_by_username(form.username.data)
            if user and check_password_hash(user['password_hash'], form.password.data):
                #2 conditions here:
                #1. user exists in UserTable
                #2. password is correct
                
                #login
                user_obj = User(user['username'], user['display_name'], user['form_group'], user['datetime_joined'], \
                    user['password_hash'], user['is_authenticated'], user['is_active'], user['is_anonymous'])
                UserTable.update_existing_user_field(user['username'], 'is_authenticated', '1')
                login_user(user_obj, remember=form.remember_me.data)
                
                #redirect to the next page
                next_page = request.args.get('next')
                if next_page and urlsplit(next_page).netloc == '':
                    return redirect(next_page)
                else:
                    return redirect(url_for('index'))
            else:
                #flash message if username or password is incorrect
                flash('Invalid username or password')
                return redirect(url_for('sign_in'))
        except:
            flash('Invalid username or password')
            return redirect(url_for('sign_in'))
        
    return render_template('sign-in.html', title='Sign In', form=form)


@app.route('/sign-out')
def sign_out():
    """
    Signs out the current user by updating their authentication status in the database
    and logging them out of the session.
    Steps:
    1. Updates the 'is_authenticated' field of the current user's record in the UserTable to '0'.
    2. Logs out the current user using the logout_user() function.
    3. Redirects the user to the sign-in page.
    Returns:
        A redirect response to the sign-in page.
    """
    
    UserTable.update_existing_user_field(current_user.username, 'is_authenticated', '0')
    logout_user()
    return redirect(url_for('sign_in'))


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Handle the user sign-up process.
    If the current user is already authenticated, they are redirected to the index page.
    Otherwise, a sign-up form is presented to the user. If the form is submitted and 
    validated (validation conditions in forms.py, not here) successfully, a new user is created in the UserTable. Upon successful 
    registration, the user is redirected to the sign-in page with a success message. 
    If an error occurs during user creation, an error message is flashed.
    Returns:
        Response: A redirect to the index page if the user is authenticated, 
                  a redirect to the sign-in page upon successful registration, 
                  or the sign-up page with the form and any error messages.
    """
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = SignUpForm()
    
    if form.validate_on_submit():
        try:
            UserTable.create_user(form.username.data, form.display_name.data, form.form_group.data, form.password.data)
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('sign_in'))
        except Exception as e:
            flash(e)
            
    return render_template('sign-up.html', title='Sign Up', form=form)

@app.route('/about')
def about():
    """
    Render the 'about' page with statistics.
    Returns:
        Response: Rendered HTML page with the following awe-inspiring statistics:
            - total_messages: Total number of messages.
            - total_invitations: Total number of invitation requests.
            - total_groups: Total number of groups.
            - total_users: Total number of users.
    """
    
    return render_template('about.html', title="About",
                           total_messages=MessageTable.get_number_of_messages(), 
                           total_invitations=InviteRequestTable.get_number_of_invite_requests(), 
                           total_groups=GroupTable.get_number_of_groups(), 
                           total_users=UserTable.get_number_of_users())


@app.errorhandler(403)
def forbidden_error(error):
    """
    Handle 403 Forbidden error.
    Args:
        error: The error object containing details about the forbidden error.
    Returns:
        rendered 403 error template and the HTTP status code 403.
    """
    
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    """
    Handle 404 Not Found error.
    Args:
        error: The error object representing the 404 Not Found error.
    Returns:
        rendered 404 error template and the HTTP status code 404.
    """
    
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Handle internal server errors by rendering a custom 500 error page.
    Args:
        error (Exception): The exception that triggered the internal server error.
    Returns:
        rendered template: A rendered 500 error template and the HTTP status code 500.
    """
    
    return render_template('500.html'), 500
from chat_app import app
from flask import render_template, flash, redirect, url_for, request, jsonify, make_response, abort
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

from datetime import datetime

from chat_app.database_operations.models import UserTable, GroupTable, UserGroupTable, MessageTable, InviteRequestTable
from werkzeug.security import check_password_hash
from chat_app.auth import User

from chat_app.forms import SignInForm, SignUpForm, BubbleForm

#validation function that returns True if string only has alphanumeric characters or spaces, false otherwise
def is_alphanumeric_or_space(string):
    for char in string:
        if not char.isalnum() and not char.isspace():
            return False
    return True


#
# APIS
#

#route to get number of online users in a group
@app.route('/number-online-users', methods = ['POST'])
def number_online_users():
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else: 
        group_id = int(request.json['group_id'])
        number_online_users = GroupTable.get_number_of_online_users(group_id)
        return make_response(jsonify(number_online_users), 200)

#route to get number of total users in a group
@app.route('/number-total-users', methods = ['POST'])
def number_total_users():
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else: 
        group_id = int(request.json['group_id'])
        number_total_users = GroupTable.get_number_of_users(group_id)
        return make_response(jsonify(number_total_users), 200)

@app.route('/group-list', methods = ['POST']) 
def group_list():
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        user_group_list = UserTable.get_user_groups(current_user.username)
        
        return make_response(jsonify(user_group_list), 200)
    
@app.route('/group-user-details', methods = ['POST'])
def group_user_details():
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        group_id = int(request.json['group_id'])
        user_list = GroupTable.get_group_user_details(group_id)
        #list of dictionaries {username, display_name, is_authenticated}
        
        return make_response(jsonify(user_list), 200)


@app.route('/all-group-messages', methods = ['POST'])
def all_group_messages():
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
    if current_user.is_authenticated == False:
        return make_response(jsonify('UNAUTHENTICATED USER'), 401)
    else:
        request_id = request.json['request_id']
        
        #update status
        InviteRequestTable.update_invite_request_status(request_id, "rejected")
        
        return make_response(jsonify('INVITE REQUEST REJECTED'), 200)


@app.route('/cancel-outgoing-invite', methods = ['POST'])
def cancel_outgoing_invite():
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
    if current_user.is_authenticated:
        return render_template('index.html', title=f'{current_user.display_name}\'s chats')
    else:
        return redirect(url_for('sign_in'))


@app.route('/chat/<group_id>')
@login_required
def chat_window(group_id):
    #check group with group_id exists
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
    subtitle = "Manage group invites here."
    if InviteRequestTable.get_number_received_invite_requests(current_user.username) == 0:
        subtitle = "Feeling lonely?"
    return render_template('invites.html', title="Group Invites", subtitle=subtitle)

@app.route('/create-group', methods=['GET', 'POST'])
def create_group():
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
                if not username.isalnum() or username not in UserTable.get_all_usernames():
                    invalid_usernames.append(username)
            
            if len(invalid_usernames) > 0:
                print(invalid_usernames)
                flash(f"Invalid usernames: {invalid_usernames}")
                return render_template('create_group.html', form=form)
            elif len(bubble_list) == 0:
                flash("Please add at least one user to the group")
                return render_template('create_group.html', form=form)
            
            elif not is_alphanumeric_or_space(group_name):
                flash("Invalid group name - only use alphanumeric characters")
                return render_template('create_group.html', form=form)
            else:
                GroupTable.create_group(group_name)
                group_id = GroupTable.get_last_group_id()
                UserGroupTable.create_user_group(current_user.username, group_id)
                
                for username in bubble_list:
                    InviteRequestTable.create_invite_request(username, current_user.username, group_id, 'pending')
                return redirect(url_for('chat_window', group_id=group_id))
                
            
            # 2. if not valid, flash message
            # 3. add element to let users add group name
            # 4. create group (add current user automatically, send invite requests to other users)
            # 5. redirect to group chat
            # 6. add notice in chat if only one person in group???????
        return render_template('create_group.html', form=form, title='Create Group')
    
    


@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
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
                user_obj = User(user['username'], user['display_name'], user['email_address'], user['datetime_joined'], \
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
    UserTable.update_existing_user_field(current_user.username, 'is_authenticated', '0')
    logout_user()
    return redirect(url_for('sign_in'))


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = SignUpForm()
    
    if form.validate_on_submit():
        UserTable.create_user(form.username.data, form.display_name.data, form.email_address.data, form.password.data)
        
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('sign_in'))
    
    return render_template('sign-up.html', title='Sign Up', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title="About",
                           total_messages=MessageTable.get_number_of_messages(), 
                           total_invitations=InviteRequestTable.get_number_of_invite_requests(), 
                           total_groups=GroupTable.get_number_of_groups(), 
                           total_users=UserTable.get_number_of_users())


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
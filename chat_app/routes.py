from chat_app import app
from flask import render_template, flash, redirect, url_for, request, jsonify, make_response, abort
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

from datetime import datetime

from chat_app.database_operations.models import UserTable, GroupTable, UserGroupTable, MessageTable, InviteRequestTable
from werkzeug.security import check_password_hash
from chat_app.auth import User

from chat_app.forms import SignInForm, SignUpForm

#
# APIS
#

@app.route('/group-list', methods = ['POST']) 
def group_list(): 
    user_group_list = UserTable.get_user_groups(current_user.username)
    
    return make_response(jsonify(user_group_list), 200)


@app.route('/all-group-messages', methods = ['POST'])
def all_group_messages():
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

# ---------------------------------------------------------------------
#                                                                     #                            
#                                                                     #
#                           ACTUAL WEBPAGE                            #
#                               ROUTES                                #  
#                                                                     #  
#                                                                     #  
# ---------------------------------------------------------------------

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
    
        return render_template('chat.html', group_display_name=group_display_name, group_id=str(group_id),  title=group_display_name)


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
def not_found_error(error):
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
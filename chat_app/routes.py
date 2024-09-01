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

@app.route('/get-username')
def get_username():
    if current_user.is_authenticated:
        return jsonify(username=current_user.username)
    return jsonify(username=None)


@app.route('/group-list', methods = ['POST']) 
def group_list(): 
    user_group_ids = UserTable.get_user_groups(current_user.username)
    
    group_name_list = []
    for id in user_group_ids:
        group_name_list.append(GroupTable.get_group_record_by_group_id(id)['group_name'])
    
    return make_response(jsonify(group_name_list), 200)


@app.route('/group-messages', methods = ['POST'])
def group_messages():
    group_id = int(request.json['group_id'])
    
    messages = GroupTable.get_all_group_messages(group_id)
    response = []
    for message in messages:
        if message[3] == current_user.username:
            usertype = 'current-user'
            sender_username = 'You'
        else:
            usertype = 'other-user'
            sender_username = message[3]

        
        response.append({
            'message_content': message[1],
            'message_date_time': message[2].strftime('%d/%m/%y %H:%M:%S'),
            'sender_username': sender_username,
            'usertype': usertype
        })
        
    return make_response(jsonify(response), 200)


@app.route('/send-message', methods = ['POST'])
def send_message():
    message_content = request.json['message_content']
    group_id = int(request.json['group'])
    sender_username = request.json['sender_username']
    
    MessageTable.create_message(message_content, sender_username, group_id)
    
    return make_response(jsonify('MESSAGE SENT'), 200)


# ROUTES

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
    if not GroupTable.get_group_record_by_group_id(group_id):
        abort(404)
    elif group_id not in UserTable.get_user_groups(current_user.username):
        abort(403)
    else:    
        group_display_name = GroupTable.get_group_record_by_group_id(group_id)['group_name']
    
        return render_template('chat.html', group_display_name=group_display_name, title=group_display_name)


@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignInForm()
    
    if form.validate_on_submit():
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


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
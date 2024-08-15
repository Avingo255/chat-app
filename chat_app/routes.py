from chat_app import app, turbo
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit

import threading, time

from chat_app.database_operations.models import UserTable, GroupTable, UserGroupTable, MessageTable, InviteRequestTable
from werkzeug.security import check_password_hash
from chat_app.auth import User

from chat_app.forms import SignInForm, SignUpForm


#LOGIN
@app.context_processor
def inject_group_record():
    group_record = GroupTable.get_group_record_by_group_id(1)
    return group_record

def update_group_list():
    with app.app_context():
        while True:
            time.sleep(1)
            print('updating group list')
            turbo.push(turbo.replace(render_template('group_list.html'), 'group_list'))


@app.route('/')
@app.route('/index')
@login_required
def index():
    threading.Thread(target=update_group_list).start()
    
    return render_template('index.html', title='Home', smth='something')


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
    return redirect(url_for('index'))


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





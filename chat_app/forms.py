from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, Field
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from wtforms.widgets import TextInput

from chat_app.database_operations.models import UserTable

def is_alphanumeric(form, field):
    if not field.data.isalnum():
        raise ValidationError('Field must be alphanumeric.')

class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), is_alphanumeric])
    display_name = StringField('Display Name', validators=[DataRequired()])
    form_group = StringField('Form Group', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        if UserTable.check_username_exists(username):
            raise ValidationError('Username already taken. Please use a different username.')


class BubbleListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return ', '.join(self.data)
        return ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',') if x.strip()]
        else:
            self.data = []
            
class BubbleForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired(), Length(max=50)])
    bubble_list = BubbleListField('Bubble List')
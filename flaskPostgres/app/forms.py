from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField,\
    TelField, TextAreaField, DateTimeField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    middle_name = StringField('Middle name')
    last_name = StringField('Last name', validators=[DataRequired()])
    post = SelectField('Post',
                       choices=[('manager', 'Manager'),( 'salaga','Regular worker')],
                       validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registration')

    def validate_email(self, email):
        pass

    def validate_username(self, username):
        pass

    def validate_phone(self, phone):
        pass


class CreationTaskForm(FlaskForm):
    id = IntegerField('Task id', validators=[DataRequired()])
    contact_person = SelectField('Contact person', choices=[])
    employee = SelectField('Executor', choices=[])
    good = SelectField('Good', choices=[])
    deadline = DateTimeField('Deadline')
    priority = StringField('Priority', validators=[DataRequired()])
    description = TextAreaField('Something about task')
    submit = SubmitField("Create task")


class TimeReportForm(FlaskForm):
    id = SelectField("Employee", choices=[])
    time_start = DateTimeField('Time start format:', validators=[DataRequired()])
    time_end = DateTimeField('Time end format:', validators=[DataRequired()])
    submit = SubmitField("Check report")

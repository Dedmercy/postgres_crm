import math
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField, \
    TelField, TextAreaField, DateTimeLocalField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    auth_form = SelectField('Auth method', choices=('mail', 'phone call'))
    # auth_form = SelectField('Auth method', choices=('mail',))
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    middle_name = StringField('Middle name')
    last_name = StringField('Last name', validators=[DataRequired()])
    post = SelectField('Post',
                       choices=[('freelancer', 'Freelancer'), ('client', 'Client')],
                       validators=[DataRequired()])
    phone = TelField('Phone', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=5, max=12,
                                                          message='Length should be between 5 and 12')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, max=16,
                                                            message='Length should be between 8 and 16')])
    confirm_password = PasswordField('Confirm your password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registration')

    def validate_email(self, field):
        if re.fullmatch(r'([\w-]+)@([a-zA-Z]+)\.([a-zA-Z]+)', field.data) is None:
            raise ValidationError("Wrong email")

    def validate_password(self, field):
        uppercase_letters: bool = False
        lowercase_letters: bool = False
        special_characters: bool = False
        numbers: bool = False
        if re.search(r'[a-z]', field.data) is not None:
            lowercase_letters = True
        if re.search(r'[A-Z]', field.data) is not None:
            uppercase_letters = True
        if re.search(r'[0-9]', field.data) is not None:
            numbers = True
        if re.search(r'[!"#$%&*+,-./:;<=>?@[\]^_`{|}]', field.data) is not None:
            special_characters = True

        if not (uppercase_letters and lowercase_letters and special_characters and numbers):
            raise ValidationError('The password must contain lowercase and uppercase Latin letters,'
                                  ' numbers, and special characters.')


class AddPerkForm(FlaskForm):
    specialization = SelectField("Specialization", choices=[])
    perk_id = SelectField("Perk", choices=[], coerce=int)
    money = IntegerField("Money")
    description = TextAreaField('Perk description')
    submit = SubmitField('Add perk')


class CreationTaskForm(FlaskForm):
    executor = IntegerField('Choose freelancer', validators=[DataRequired()])
    deadline = StringField('Deadline', validators=[DataRequired()])
    description = TextAreaField('Task description')
    submit = SubmitField('Create task')

    def validate_deadline(self, field):
        if re.fullmatch('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', field.data) is None:
            raise ValidationError('The deadline must match the pattern "YYYY-mm-dd hh:mm:ss"')


class AddReviewForm(FlaskForm):
    review_header = StringField('Заголовок отзыва')
    review_text = TextAreaField('Описание отзыва')
    review_mark = SelectField("Оценка", choices=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

    submit = SubmitField('Add Review')


class FindFreelancerByPerkForm(FlaskForm):
    specialization = SelectField("Specialization", choices=[])
    perk = SelectField("Perk", choices=[])
    submit = SubmitField('Choose executor')


class ReportsForm(FlaskForm):
    task = SelectField("Task", choices=[], validators=[DataRequired()])
    submit = SubmitField("Show info")


class CreateEditingForm(FlaskForm):
    task = SelectField("Task", choices=[], validators=[DataRequired()])
    num = IntegerField('Editing number', validators=[DataRequired()])
    header = StringField('Header', validators=[DataRequired(),
                                               Length(max=20, message="Header length must be less than 20")])
    text = TextAreaField('Editing description')
    submit = SubmitField("Show info")


class IntLength:
    """
    Validates the length of a string.

    :param min:
        The minimum required length of the string. If not provided, minimum
        length will not be checked.
    :param max:
        The maximum length of the string. If not provided, maximum length
        will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)d` and `%(max)d` if desired. Useful defaults
        are provided depending on the existence of min and max.

    When supported, sets the `minlength` and `maxlength` attributes on widgets.
    """

    def __init__(self, min=-1, max=-1, message=None):
        assert (
                min != -1 or max != -1
        ), "At least one of `min` or `max` must be specified."
        assert max == -1 or min <= max, "`min` cannot be more than `max`."
        self.min = min
        self.max = max
        self.message = message
        self.field_flags = {}
        if self.min != -1:
            self.field_flags["minlength"] = self.min
        if self.max != -1:
            self.field_flags["maxlength"] = self.max

    def __call__(self, form, field):
        length = field.data and len(str(field.data)) or 0
        if length >= self.min and (self.max == -1 or length <= self.max):
            return

        if self.message is not None:
            message = self.message

        elif self.max == -1:
            message = field.ngettext(
                "Field must be at least %(min)d character long.",
                "Field must be at least %(min)d characters long.",
                self.min,
            )
        elif self.min == -1:
            message = field.ngettext(
                "Field cannot be longer than %(max)d character.",
                "Field cannot be longer than %(max)d characters.",
                self.max,
            )
        elif self.min == self.max:
            message = field.ngettext(
                "Field must be exactly %(max)d character long.",
                "Field must be exactly %(max)d characters long.",
                self.max,
            )
        else:
            message = field.gettext(
                "Field must be between %(min)d and %(max)d characters long."
            )

        raise ValidationError(message % dict(min=self.min, max=self.max, length=length))


class SecondAuth(FlaskForm):
    number = IntegerField('Editing number', validators=[DataRequired(), IntLength(4)])
    submit = SubmitField("Log in")

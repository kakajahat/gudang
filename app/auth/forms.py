from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Pengguna


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    uname = StringField('User Name', validators=[DataRequired()])
    name = StringField('Nama Lengkap', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired(), 
                                                EqualTo('confirm_password')
                                                ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')
    
    def validate_email(self, field):
        if Pengguna.query.filter_by(email=field.data).first():
            raise ValidationError('Email telah di gunakan.')
            
    def validate_uname(self, field):
        if Pengguna.query.filter_by(uname=field.data).first():
            raise ValidationError('Username sudah di gunakan.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    passwd = PasswordField('Uname', validators=[DataRequired()])
    submit = SubmitField('Login')
    

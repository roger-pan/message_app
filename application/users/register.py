from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from application.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired()]
                            )

    email = StringField('Email', 
                        validators=[DataRequired(), 
                        Email()]
                        )

    first_name = StringField('First Name',
                            validators=[DataRequired()]
                            )
    
    last_name = StringField('Last Name',
                            validators=[DataRequired()]
                            )

    password = PasswordField('Password',
                            validators=[DataRequired()]
                            )

    password2 = PasswordField('Repeat Password',
                            validators=[DataRequired(),
                            EqualTo('password')
                            )
    

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken. Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email registered. Please use a different email address, or, login.')
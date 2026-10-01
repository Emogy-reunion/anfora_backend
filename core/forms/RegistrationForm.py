from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    company_name = StringField("Company Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    admin_firstname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    admin_lastname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=50)])
    phone_number = StringField("Phone Number", validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    #website=StringField("Website", validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
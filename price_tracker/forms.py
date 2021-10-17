from flask_wtf.form import FlaskForm


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo


class SearchForm(FlaskForm) :

    url = StringField('Enter The Amazon Product URL')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = StringField("Email : ", validators=[ Email("Please Enter valid email"), InputRequired("Please Enter your email")])
    password = PasswordField("Please Enter your password : ", validators=[InputRequired('Password Should not be empty'), EqualTo('confirm', 'passwords must match !')])
    confirm = PasswordField(" Re Enter your password : ")

    submit = SubmitField("Create Account ?")
    


class LoginForm(FlaskForm):
    email = StringField("Email : ", validators=[ Email("Please Enter valid email"), InputRequired("Please Enter your email")])
    password = PasswordField("Please Enter your password : ", validators=[InputRequired('Password Should not be empty'), 
                ])

    submit = SubmitField("Login")





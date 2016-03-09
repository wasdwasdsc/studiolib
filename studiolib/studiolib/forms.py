from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    e_mail = StringField('e_mail', validators=[DataRequired()])
    pw = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class RegisterForm(Form):
    e_mail = StringField('e_mail', validators=[DataRequired()])
    pw = StringField('password', validators=[DataRequired()])

class AddForm(Form):
    a_name = StringField('a_name', validators=[DataRequired()])
    b_name = StringField('b_name', validators=[DataRequired()])

class SearchForm(Form):
    text = StringField('text', validators=[DataRequired()])
    by_author = BooleanField('by_author', default=False)
    by_book = BooleanField('by_book', default=False)

class EditForm(Form):
    text = StringField('text', validators=[DataRequired()])
    new_text = StringField('new_text', validators=[DataRequired()])
    by_author = BooleanField('by_author', default=False)
    by_book = BooleanField('by_book', default=False)
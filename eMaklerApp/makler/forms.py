from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from makler.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Użytkownik o podanej nazwie już istnieje! Spróbuj innej nazwy!')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Podany e-mail jest już w użyciu! Spróbuj innego e-maila!')

    username = StringField(label='Nazwa użytkownika:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Adres e-mail:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Hasło:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Potwierdź hasło:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Stwórz konto')

class LoginForm(FlaskForm):
    username = StringField(label='Nazwa użytkownika:', validators=[DataRequired()])
    password = PasswordField(label='Hasło:', validators=[DataRequired()])
    submit = SubmitField(label='Zaloguj')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Kup akcje!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sprzedaj akcje!')
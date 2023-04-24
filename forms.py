from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, EmailField, PasswordField
from wtforms.validators import DataRequired


# форма авторизации.
class LoginForm(FlaskForm):
    # поле почты
    email = EmailField('Почта', validators=[DataRequired()])
    # поле пароля
    password = PasswordField('Пароль', validators=[DataRequired()])
    # поле для запоминания пользователя.
    remember_me = BooleanField("Запомнить меня")
    # кнопка войти
    submit = SubmitField("Войти")


# форма регистрации.
class RegisterForm(FlaskForm):
    # поле почты
    email = EmailField('Почта', validators=[DataRequired()])
    # поле пароля
    password = PasswordField('Пароль', validators=[DataRequired()])
    # поле повтореного пароля
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    # поле имени
    name = StringField('Имя пользователя', validators=[DataRequired()])
    # поле фамилии
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    # кнопка зарегестрироваться
    submit = SubmitField('Зарегестрироваться')


# форма настроек
class EditForm(FlaskForm):
    # поле пароля
    password = PasswordField('Пароль', validators=[DataRequired()])
    # поле повтореного пароля
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    # поле имени
    name = StringField('Имя пользователя', validators=[DataRequired()])
    # поле фамилии
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    # кнопка сохранить.
    submit = SubmitField('Сохранить')


# форма сообщения.
class InputForm(FlaskForm):
    text = StringField(validators=[DataRequired()])
from flask import request, Flask, redirect, render_template
from data.user import User
from data.db_session import create_session, global_init
from flask_login import LoginManager, login_user, logout_user,\
    login_required, AnonymousUserMixin, current_user
from forms import LoginForm, RegisterForm, EditForm, InputForm


# файл main - гланый файл приложения
# app - объект класса Flask
app = Flask(__name__)
# создание ключа - yandexlyceum_secret_key
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# login_manager - объект класса LoginManager, позволяющий работать с пользователями
login_manager = LoginManager()
login_manager.init_app(app)
# инициализация базы данных
global_init('db/chat.db')


# load_user возвращает полученного пользователя
@login_manager.user_loader
def load_user(user_id):
    # создане сессии
    db_sess = create_session()
    # возврат пользователя.
    return db_sess.query(User).get(user_id)


# logout вызывает функцию logout_user, которая позволяет пользователю выйти
@app.route('/logout')
@login_required
def logout():
    # выход пользователя.
    logout_user()
    # перенаправление пользователя на главную страницу.
    return redirect("/")


# messages - список всех сообщений
messages = []


# send_message получает сообщение и добавляет его в список сообщений
def send_message(user, message):
    global messages
    # если в сообщении есть символы.
    if message:
        # mes хранит в себе сообзение разбитое на части
        mes = ['']
        for i in range(0, len(message)):
            # если длина сообщения больше 88, то оно разбивается отступами.
            if i % 88 == 0 and i:
                mes.append('')
            mes[-1] += message[i]
        name = f'{user.name} {user.surname}: '
        # добавление в список отправителя и само сообщение.
        messages.append(name + '\n'.join(mes))


# функция main отвечает за работу главного окна и чата
@app.route('/', methods=['GET', "POST"])
def main():
    global messages
    # если пользователь не авторизован, то страница будет пустой.
    if not current_user.is_authenticated:
        return render_template('base.html', title='Chat')
    # создание формы.
    form = InputForm()
    # в случае отправки сообщения вызывается функция send_message и обновление страницы.
    if request.method == 'POST':
        send_message(current_user, form.text.data)
        return render_template('chat.html', messages=messages, send_message=send_message, form=form, title='Chat')
    # если ничего не случилось, то чат просто загружается.
    return render_template('chat.html', messages=messages, send_message=send_message, form=form, title='Chat')


# функция login вызывает форму авторизации и контролирует ее.
@app.route('/login', methods=['GET', "POST"])
def login():
    # создание формы.
    form = LoginForm()
    # если пользователь пытается войти.
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        # проверка на правильность пароля, если да, то пользователя перенаправляют на главную страницу.
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        # если нет, то выводится ошибка.
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Авторизация')
    # перенаправление на страницу (если метод GET).
    return render_template('login.html', form=form, title='Авторизация')


# register вызывает форму регистрации пользователя
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    # создание формы.
    form = RegisterForm()
    # если кнопка нажата.
    if form.validate_on_submit():
        # если пароли не совпадают, то пользователь должен ввести их снова.
        if form.password.data != form.password_again.data:
            # обновление страницы.
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = create_session()
        # если пользователь с данным email есть, то он не может зарегистрироваться.
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        # в случае успеха создается объект класса User и заносится в базу данных.
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data
        )
        # пользователю задают пароль и сохраняют его.
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        # перенаправление на страницу авторизации.
        return redirect('/login')
    # перенаправление на страницу (при методе GET).
    return render_template('register.html', title='Регистрация', form=form)


# edit вызывает форму, позволяющая изменить пользователя или удалить
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    # создание формы.
    form = EditForm()
    if form.validate_on_submit():
        # если новые пароли не совпадают, то выводится ошибка.
        if form.password.data != form.password_again.data:
            # обновление страницы.
            return render_template('edit.html', title='Настройки',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = create_session()
        # если все прошло удачно, то пользователь корректируется.
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        # сохраниение пароля.
        user.set_password(form.password.data)
        # сохраниение имени.
        user.name = form.name.data
        # сохраниение фамилии.
        user.surname = form.surname.data
        db_sess.commit()
        # перемещение на главную страницу.
        return redirect('/')
    return render_template('edit.html', form=form)


# delete удаляет пользователя.
@app.route('/delete')
def delete():
    # если пользователь авторизован.
    if current_user.is_authenticated:
        db_sess = create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        # удаление пользователя.
        db_sess.delete(user)
        db_sess.commit()
        # перенаправление на главную страницу.
        return redirect('/')
    else:
        # перенаправление на главную страницу.
        return redirect('/')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
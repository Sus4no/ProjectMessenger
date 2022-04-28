from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
from data.messages import Messages
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from bcrypt import hashpw


app = Flask(__name__)
app.config['SECRET_KEY'] = 'duAMjLz8HhvBLjllrCTy'
SALT = b'$2b$12$rQ4fJyk5g7baIrXABXO3nu'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            user = User()
            user.username = form.username.data
            user.password = hashpw(form.password.data.encode(), SALT)

            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('registration.html', title='Регистрация', form=form)
    return redirect("/contacts")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            password = hashpw(form.password.data.encode(), SALT)
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.username == form.username.data).first()

            if user and user.password == password:
                login_user(user, remember=form.remember_me.data)
                return redirect('/contacts')
            
            return render_template('login.html', message="Неправильный логин или пароль", form=form)
        return render_template('login.html', title='Авторизация', form=form)
    return redirect("/contacts")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/contacts', methods=['GET', 'POST'])
def contacts_page():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        users = set()
        messages = db_sess.query(Messages).filter((Messages.sender == current_user.username) | (Messages.receiver == current_user.username)).all()
        for i in messages:
            users.add(i.sender)
            users.add(i.receiver)
            users.remove(current_user.username)
        if request.method == 'POST':
            add_contact = request.form.get('add_contact')
            add_message = request.form.get('add_message')
            usernames = db_sess.query(User).all()
            for item in usernames:
                if add_contact == item.username:
                    message = Messages()
                    message.sender = current_user.username
                    message.receiver = add_contact
                    message.text = add_message
                    db_sess.add(message)
                    db_sess.commit()
                    return render_template('contacts.html', users=users, current_user=current_user)
        return render_template('contacts.html', users=users, current_user=current_user)
    return redirect("/login")


@app.route('/contacts/<username>', methods=['GET', 'POST'])
def dialogue_page(username):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        messages = db_sess.query(Messages).filter((Messages.sender == current_user.username) | (Messages.receiver == current_user.username),
        (Messages.sender == username) | (Messages.receiver == username ))

        if request.method == 'POST':
            cur_mess = request.form.get('cur_mess')
            message = Messages()
            message.sender = current_user.username
            message.receiver = username
            message.text = cur_mess
            db_sess.add(message)
            db_sess.commit()
            return render_template('conversation.html', messages=messages[::-1])
        return render_template('conversation.html', messages=messages[::-1])
    return redirect("/login")


def main():
    db_session.global_init('db/users.db')
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()

from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
import bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'duAMjLz8HhvBLjllrCTy'
users = ['user1', 'user2', 'user3', 'user4', 'user5']
messages = ['Lorem ipsum dolor', '2', 'Some txt', '4', 'etc']
SALT = b'$2b$12$rQ4fJyk5g7baIrXABXO3nu'


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = LoginForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.password = bcrypt.hashpw(form.password.data.encode(), SALT)
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()

        user1 = db_sess.query(User).all()
        for i in user1:
            print(i.username, i.password)
        
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        password = bcrypt.hashpw(form.password.data.encode(), SALT)
        user.password = password
        db_sess = db_session.create_session()

        for username in db_sess.query(User).filter(User.username == form.username.data):
            if username.password == password:
                return redirect('/contacts')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/purge')
def clear():
    db_sess = db_session.create_session()
    db_sess.query(User).delete()
    for i in db_sess.query(User).all():
        print(i.username)
    db_sess.commit()
    return 'Done'


@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html', users=users)


@app.route('/contacts/<user_id>')
def dialogue_page(user_id):
    return render_template('conversation.html', messages=messages)


def main():
    db_session.global_init('db/users.db')
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()

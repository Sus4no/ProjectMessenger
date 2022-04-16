from flask import Flask, render_template, request


app = Flask(__name__)
users = ['user1', 'user2', 'user3', 'user4', 'user5']
messages = ['Lorem ipsum dolor', '2', 'Some txt', '4', 'etc']


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html', users=users)


@app.route('/contacts/<user_id>')
def dialogue_page(user_id):
    return render_template('conversation.html', messages=messages)


def main():
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()

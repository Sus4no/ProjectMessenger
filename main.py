from flask import Flask, render_template, request


app = Flask(__name__)
users = ['user1', 'user2', 'etc']


# @app.route('/')
# def welcome_page():
#     return render_template('welcome.html')


@app.route('/contacts')
def main_page():
    return render_template('main.html', users=users)


def main():
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()

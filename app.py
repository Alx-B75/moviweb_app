from flask import Flask, render_template, redirect, url_for, request
from datamanager.sqlite_data_manager import SQLiteDataManager, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviwebapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

data_manager = SQLiteDataManager(app)


@app.route('/')
def home():
    return "<h1>Welcome to MoviWeb App</h1>"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            data_manager.add_user(name)
            return redirect(url_for('list_users'))
    return render_template('add_user.html')


if __name__ == '__main__':
    app.run(debug=True)

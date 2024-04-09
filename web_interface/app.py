from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os
from pycode.chat import Chat

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/RAG"
mongo = PyMongo(app)
app.secret_key = os.urandom(16)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_mail = users.find_one({'email': request.form['email']})
        existing_username = users.find_one({'username': request.form['username']})

        if existing_mail is None and existing_username is None:
            if request.form['password'] != request.form['confirm_password']:
                session['password_match'] = False
                return redirect(url_for('login_page', password_match='1'))
            else:
                hashpass = generate_password_hash(request.form['password'])
                users.insert_one(
                    {'username': request.form['username'], 'email': request.form['email'], 'password': hashpass})
                return redirect(url_for('index'))

        if existing_mail:
            session['email_exists'] = True
            return redirect(url_for('login_page', email_exists='1'))

        if existing_username:
            session['username_exists'] = True
            return redirect(url_for('login_page', username_exists='1'))

    return redirect(url_for('login_page'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'email': request.form['email']})

        if login_user is None or not check_password_hash(login_user['password'], request.form['password']):
            flash('E-Mail oder Passwort inkorrekt', 'danger')
            return redirect(url_for('login_page'))

        # Setzen des 'username' in der Session nach erfolgreicher Authentifizierung
        session['username'] = login_user['username']

        # Generieren einer eindeutigen Session-ID
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id

        # Weiterleitung zum Hauptbereich der Anwendung
        return redirect(url_for('index'))


@app.route('/')
def login_page():
    return render_template('login_page.html')


@app.route('/index')
def index():
    if 'username' in session:
        return render_template('chat.html', username=session['username'])
    else:
        return redirect(url_for('login_page'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('session_id', None)
    return redirect(url_for('index'))


@app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        data = request.json
        user_message = data.get('user_message', '')  # Sicherer Zugriff auf 'user_message'
        if 'username' in session:
            chat = Chat()
            response = chat.create_chat(user_message)
            return jsonify({'response': response.content})

        else:
            return jsonify({'response': 'Session nicht gefunden. Bitte erneut anmelden.'}), 403




if __name__ == '__main__':
    app.run(debug=True)

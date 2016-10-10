from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
import hashlib
engine = create_engine('sqlite:///datos.db', echo=True)

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login_form.html')
    else:
        return render_template('logged_in.html')

@app.route('/register', methods=['GET'])
def register_show_form():
    if not session.get('logged_in'):
        return render_template('registration.html')
    else:
        return redirect(url_for('home'))

@app.route('/register', methods=['POST'])
def register():
    formdata = request.form
    given_username = formdata["username"]
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([given_username]))
    result = query.first()

    if result:
        return render_template('registrationerror.html')
    else:
        password_digest = hashlib.sha224(str(formdata["password"]).encode('utf-8')).hexdigest()
        #
        Session = sessionmaker(bind=engine)
        session = Session()
        user = User(formdata["username"],password_digest,formdata["firstname"], formdata["lastname"], formdata["email"])
        session.add(user)
        session.commit()

        return render_template('registered.html')


@app.route('/login', methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = hashlib.sha224(str(request.form['password']).encode('utf-8')).hexdigest()

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
        session['username'] = result.username
    else:
        session['logged_in'] = False
        print("sdfgjnsa")
        return render_template('loginerror.html')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)

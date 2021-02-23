from app import app
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for, session, request
from database.db_access import DataAccess


db = SQLAlchemy(app)
db_conn = DataAccess()


@app.route('/')
@app.route('/index')
def home():
    if 'id' in session:
        user_data = session['id']
        return render_template("home.html", user=user_data)
    else:
        return render_template("index.html")

@app.route('/custLogin', methods=["POST"])
def custLogin():
    if request.method == "POST":

        email = request.form['email']
        password = request.form['password']

        if email and password:
            cust_id = db_conn.customerLogin(email, password)
            if(cust_id):
                session['id'] = cust_id
                return redirect(url_for('index'))
            else:
                return render_template("index.html", error='ERROR')
        else:
            return render_template("index.html", error='ERROR')


@app.route('/signup', methods=['POST'])
def signup():

    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    password = request.form['password']
    address = request.form['address']
    town = request.form['town']
    parish = request.form['parish']

    id = db_conn.signup(firstName, lastName, email, password, address, town, parish)
    if(id):
        session['id'] = id
        return redirect(url_for('index'))
    return render_template('error.html', error="signup error has occured")


@app.route('/employLogin', methods=["POST"])
def employLogin():
    if request.method == "POST":

        email = request.form['email']
        password = request.form['password']

        if email and password:
            cust_id = db_conn.customerLogin(email, password)
            if(cust_id):
                session['id'] = cust_id
                return redirect(url_for('index'))
            else:
                return render_template("index.html", error='ERROR')
        else:
            return render_template("index.html", error='ERROR')


@app.route('/logout', methods=["GET", "POST"])
def logout():
    if 'id' in session:
        session.pop('id', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


# if __name__ == "__main__":
#     app.run(debug=True,host="0.0.0.0")
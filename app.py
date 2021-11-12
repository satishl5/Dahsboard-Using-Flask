import os
from flask import Flask,render_template,request, session,url_for
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'secret'

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable = False)
    city = db.Column(db.String(200),nullable = False)
    password = db.Column(db.String(100),nullable = False)

    def __repr__(self) -> str:
        return '<Users %r>' % self.id

@app.route('/', methods =['GET', 'POST'])
@app.route('/index', methods =['GET', 'POST'])
def index():
    if request.method == 'POST':
        uname = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=uname).first()
        if user and user.username == uname and user.password == password:
            session['loggedin'] = True
            session['id'] = user.id
            if uname == "Admin" and password == "Admin":
                return redirect(url_for('admin'))
            return render_template('profile.html',user = user)
        else:
            msg = "Invalid Credentials"
            return render_template('index.html',msg=msg)
    return render_template('index.html')

@app.route("/admin")
def admin():
    uname = 'Admin'
    users = Users.query.filter(Users.username!=uname).all()
    return render_template('admin.html',users=users)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/register",methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        email = request.form['email']
        city = request.form['city']
        password = request.form['password']
        if len(uname) < 1 and len(email) < 1 and len(city) < 1 and len(city) < 1:
            msg = "Invalid Details"
            return render_template('register.html',msg=msg)
        new_user = Users(username=uname,email=email,city=city,password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return e

    return render_template('register.html')


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for('admin'))
    except:
        return "There was an issue deleting the user"

if __name__ == '__main__':
    app.run()
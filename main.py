from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import data_required
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user-database.db"
db.init_app(app)
Bootstrap5(app)
app.secret_key = "ANY_SECRET_KEY"


class UserLog(FlaskForm):
    user_name = StringField('Username', validators=[data_required()])
    password = PasswordField('Password', validators=[data_required()])
    submit = SubmitField('Submit')


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), unique=False, nullable=False)
    lname = db.Column(db.String(50), unique=False, nullable=False)
    country = db.Column(db.String(50), unique=False, nullable=False)
    city = db.Column(db.String(50), unique=False, nullable=False)
    state = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/users')
def show_users():
    with app.app_context():
        user_list = db.session.execute(db.select(UserData).order_by(UserData.id)).scalars()
        db.session.commit()
        return render_template('users.html', user_list=user_list)


@app.route('/sign-up')
def sign_up():
    return render_template('sign_up.html')


@app.route('/sign-up-process', methods=["GET", "POST"])
def sign_up_check():
    with app.app_context():
        print(request.form.get('fname'))
        print(request.form.get('lname'))
        print(request.form.get('email'))

        new_user = UserData(fname=request.form.get('fname'), lname=request.form.get('lname'),
                            country=request.form.get('country'), city=request.form.get('city'),
                            state=request.form.get('state'), email=request.form.get('email'),
                            phone=request.form.get('phone'), age=request.form.get('age'),
                            user_name=request.form.get('username'), password=request.form.get('password'))
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete', methods=["GET", "POST"])
def delete():
    form = UserLog()
    user_id = request.args.get('id')
    user_select = db.get_or_404(UserData, user_id)
    if form.validate_on_submit():
        if form.user_name.data == user_select.user_name and form.password.data == user_select.password:
            db.session.delete(user_select)
            db.session.commit()
            return redirect(url_for('show_users'))
    return render_template('login.html', form=form, mode="delete")


@app.route('/login', methods=["GET", "POST"])
def login():
    form = UserLog()
    user_data = db.session.execute(db.select(UserData).order_by(UserData.user_name)).scalars()
    for a_user in user_data:
        if form.user_name.data == a_user.user_name and form.password.data == a_user.password:
            logged_user = db.session.execute(db.select(UserData).where(UserData.user_name
                                                                       == form.user_name.data)).scalar()
            # db.get_or_404(UserData, form.user_name.data)
            return render_template('dashboard.html', log_user=logged_user)
    return render_template('login.html', form=form, mode="login")


app.run(debug=True)

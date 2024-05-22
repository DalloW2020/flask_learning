from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it-is-a-secret-key-for-test-purposes'
#adding database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#init db
db = SQLAlchemy(app)
app.app_context()


# Create database model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Name %r>' % self.name


class NameForm(FlaskForm):
    name = StringField('Enter Name', validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template('add_user.html')

#
# @app.route('/user/<name>')
# def user(name):
#     return render_template('add_user.html', name=name)


#invalid URL
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# @app.route('/name', methods=['GET', 'POST'])
# def name():
#     name = None
#     form = NameForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ""
#         flash('Form Submitted Successfully')
#     return render_template('name.html',
#                            form=form,
#                            name=name)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = NameForm()
    name = None
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        flash('User added to DataBase')
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
                           form=form,
                           name=name,
                           our_users=our_users)


if __name__ == '__main__':
    app.run(debug=True)

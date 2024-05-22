from flask import Flask, render_template, flash,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'it-is-a-secret-key-for-test-purposes'
#adding database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#init db
db = SQLAlchemy(app)
app.app_context()
migrate = Migrate(app, db)
"""
Flask migrate commands:
flask db migrate -m "enter a tag"
flask db upgrade
"""

# Create database model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favorite_color = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.now())
    # password stuff
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name


class NameForm(FlaskForm):
    name = StringField('Enter Name', validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    favorite_color = StringField('Favorite Color')
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
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.favorite_color.data = ""
        flash('User added to DataBase')
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
                           form=form,
                           name=name,
                           our_users=our_users)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    form = NameForm()
    name = None
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted!!')
        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html',
                               form=form,
                               name=name,
                               our_users=our_users)
    except:
        flash('Seems there was a problem with the delete... Please try again')
        our_users = Users.query.order_by(Users.date_added)
        return render_template('add_user.html',
                               form=form,
                               name=name,
                               our_users=our_users)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user_to_update = Users.query.get_or_404(id)
    form = NameForm()
    name = None
    if request.method == "POST":
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        user_to_update.favorite_color = request.form['favorite_color']
        try:
           db.session.commit()
           flash('Update Record Successfully')
           return render_template('update.html',
                                  form=form,
                                  user_to_update=user_to_update)
        except:
            flash('Update Record Error')
            return render_template('update.html',
                                   form=form,
                                user_to_update=user_to_update)
    else:
        return render_template('update.html',
                               form=form,
                               user_to_update=user_to_update)
if __name__ == '__main__':
    app.run(debug=True)

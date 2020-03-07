from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users, Skills
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, Details

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dashboard'))


@app.route('/update_skill', methods=['GET', 'POST'])
def update_skill():
    if request.method == 'POST':
        o=request.get_data()
        loc = request.form['rating']
        print(loc)
        return redirect('dashboard')
    return render_template('update_skill.html', title='Update Skill')


@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html', title='Search')

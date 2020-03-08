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
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dashboard'))


@app.route('/update_skill', methods=['GET', 'POST'])
def update_skill():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = dict(request.form)
        x = int((len(data)-2)/3)
        print(data,x)
        for i in range(1, x+1):
            s = Skills(employee_id=current_user.emp_id, skill=data['skills'+str(i)], skill_exp=data['experience'+str(i)],emp_rating=data['rating'+str(i)])
            db.session.add(s)
            db.session.commit()
        u = Users.query.filter_by(emp_id=current_user.emp_id).first()
        u.practice = data['practice']
        u.location = data['location']
        db.session.commit()
        return redirect('dashboard')
    return render_template('update_skill.html', title='Update Skill')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        data = dict(request.form)
        x = int(len(data)/3)
        print(data,x)
        z = []
        p = []
        for i in range(1, x+1):
            t = db.session.query(Skills.employee_id).filter(Skills.skill == data['skills'+str(i)], Skills.skill_exp >= data['experience'+str(i)],
                                    (Skills.emp_rating + Skills.manager_rating)/2 >= int(data['rating'+str(i)])).all()
            z.append(t)
        print("query: ", z)
        for i in range(len(z)-1):
            if i == 0:
                p = list(set(z[i]) & set(z[i+1]))
            else:
                p = list(set(p) & set(z[i+1]))
        res = []
        for t in p[0]:
            res.append(Users.query.filter_by(emp_id=t).first())
        print("search result: ", res)
    return render_template('search.html', title='Search')

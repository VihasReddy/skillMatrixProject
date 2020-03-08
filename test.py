from app import db
from app.models import Users, Skills

"""
db.session.query(Users).delete()
db.session.commit()

u1 = Users(emp_id='T0100', username='Vihas', email='vihasreddy@enquero.com', overall_exp=3, manager_id='T0099')
u2 = Users(emp_id='T0101', username='Jagruth', email='jagruth@enquero.com', overall_exp=2, manager_id='T0100')
u3 = Users(emp_id='T0102', username='Pruthvi', email='pruthvi@enquero.com', overall_exp=4, manager_id='T0100')
u4 = Users(emp_id='T0099', username='Mahantesh.R', email='mahantesh@enquero.com', overall_exp=5, manager_id='T9999')
u1.set_password('1234')
u2.set_password('1234')
u3.set_password('1234')
u4.set_password('1234')
db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.add(u4)
db.session.commit()
"""

users = Users.query.all()

for u in users:
    print(u)

"""
db.session.query(Skills).delete()
db.session.commit()

a = db.engine.execute('insert into Skills (emp_id,skill,experience,emp_rating) values ("E1", "java", 3, 9)')
b = db.engine.execute('insert into Skills (emp_id,skill,experience,emp_rating) values ("E2", "python", 2, 10)')
c = db.engine.execute('insert into Skills (emp_id,skill,experience,emp_rating) values ("E3", "C", 4, 7)')
d = db.engine.execute('insert into Skills (emp_id,skill,experience,emp_rating) values ("E4", "python", 3, 9)')
e = db.engine.execute('insert into Skills (emp_id,skill,experience,emp_rating) values ("X1", "python", 2, 8)')
db.session.commit()
"""

skills = Skills.query.all()

for i in skills:
    print(i)

current_user = Users.query.filter_by(emp_id="T0100").first()

r = db.engine.execute('select * from Users where emp_id IN (select employee_id from Skills where skill_exp >= 3)').fetchall()
x = db.engine.execute('select username from Users where overall_exp > '+str(2)).fetchall()
# y = db.engine.execute('select emp_id from Users where manager_id LIKE 'T0100').fetchall()

q = Skills.query.filter_by(manager_rating=None).join(Users).filter_by(manager_id=current_user.emp_id).all()


for res in q:
    print("Update {} for {} skill ".format(res.employee_id, res.skill))
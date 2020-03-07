from app import db
from app.models import Users, Skills

users = Users.query.all()

skills = Skills.query.all()

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

for i in skills:
    print(i)

r = db.engine.execute('select * from Users where emp_id IN (select employee_id from Skills where skill_exp >= 3)').fetchall()
x = db.engine.execute('select username from Users where overall_exp > 2').fetchall()
print(r)
print(x)

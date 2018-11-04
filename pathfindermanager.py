# Python 3.6 Code
import os
import datetime
from flask import Flask, redirect, session
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "pf.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


class Pathfinder(db.Model):
	id = db.Column(
    db.String(100),
    nullable=False,
    primary_key=True,
    unique=True,
     autoincrement=False)
	firstname = db.Column(db.String(80), nullable=False)
	lastname = db.Column(db.String(80), nullable=False)
	middlename = db.Column(db.String(80), nullable=True)
	addr = db.Column(db.String(80), nullable=False)
	school = db.Column(db.String(80), nullable=True)
	fname = db.Column(db.String(80), nullable=True)
	phone = db.Column(db.Integer, nullable=True)
	batch = db.Column(db.String(4), nullable=True)
	dob = db.Column(db.String(10), nullable=True)
	dateAdd = db.Column(db.String(10), nullable=False)
	optradio = db.Column(db.String(10), nullable=False)
	cls = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return "<ID & Name  {} >".format(str(self.id))


class Reg(db.Model):
	id = db.Column(
    db.String(100),
    nullable=False,
    primary_key=True,
    unique=True,
     autoincrement=False)
	firstname = db.Column(db.String(80), nullable=False)
	lastname = db.Column(db.String(80), nullable=False)
	january = db.Column(db.Boolean, default=False)
	february = db.Column(db.Boolean, default=False)
	march = db.Column(db.Boolean, default=False)
	aprill = db.Column(db.Boolean, default=False)
	may = db.Column(db.Boolean, default=False)
	june = db.Column(db.Boolean, default=False)
	july = db.Column(db.Boolean, default=False)
	august = db.Column(db.Boolean, default=False)
	september = db.Column(db.Boolean, default=False)
	october = db.Column(db.Boolean, default=False)
	november = db.Column(db.Boolean, default=False)
	december = db.Column(db.Boolean, nullable=False, default=False)
	january_invoice = db.Column(db.Integer, default=False)
	february_invoice = db.Column(db.Integer, default=False)
	march_invoice = db.Column(db.Integer, default=False)
	aprill_invoice = db.Column(db.Integer, default=False)
	may_invoice = db.Column(db.Integer, default=False)
	june_invoice = db.Column(db.Integer, default=False)
	july_invoice = db.Column(db.Integer, default=False)
	august_invoice = db.Column(db.Integer, default=False)
	september_invoice = db.Column(db.Integer, default=False)
	october_invoice = db.Column(db.Integer, default=False)
	november_invoice = db.Column(db.Integer, default=False)
	december_invoice = db.Column(db.Integer, default=False)

	def __repr__(self):
		return "<ID {} >".format(str(self.id))


app.secret_key = "something random"


@app.route('/login', methods=['POST', "GET"])
def do_admin_login():
	if request.method == "POST":
		if request.form['password'] == 'Secret55!' and request.form['username'] == 'noname':
			session['logged_in'] = True
			return redirect("/")
		else:
			return "<h1>wrong password or username Try Again:? <a href='/login'>Go to login page</a></h1>"
	else:
		return render_template("/login.html")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect("/login")


@app.route("/regi", methods=["POST", "GET"])
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	if request.method == "POST":
		fn = request.form.get("firstname")
		ln = request.form.get("lastname")
		mn = request.form.get("middlename")
		addr = request.form.get("addr")
		school = request.form.get("school")
		fname = request.form.get("fname")
		phone = request.form.get("phone")
		batch = request.form.get("batch")
		dateAdd = request.form.get("dateAdd")
		cls = request.form.get("cls")
		dob = request.form.get("dob")
		optradio = request.form.get("optradio")
		pathfinder = Pathfinder(
    id=fn +
    ln +
    str(phone) +
    dateAdd,
    firstname=fn,
    lastname=ln,
    middlename=mn,
    addr=addr,
    phone=phone,
    school=school,
    cls=cls,
    fname=fname,
    batch=batch,
    dateAdd=dateAdd,
    optradio=optradio,
     dob=dob)
		pt = Pathfinder.query.filter_by(
    id=fn + ln + str(phone) + str(dateAdd),
    ).all()  # queries for that particular record in the db
		# print(pt)
		if(len(pt) == 0):  # if the record is not alrdy there it add's it
			db.session.add(pathfinder)
			db.session.commit()
			temp = Reg(id=fn + ln + str(phone) + dateAdd, firstname=fn, lastname=ln)
			db.session.add(temp)
			db.session.commit()
			return redirect("/")
		else:
			return '<h1>Error Record with same FirstName Lastname Phone and DOB exists</h1>'
	else:
		return render_template("regi.html")


@app.route("/", methods=["POST", "GET"])
def pay():
    if not session.get('logged_in'):
        return render_template('login.html')
    if request.method == "POST":
        id = request.form.get("id")
        amount = request.form.get("amount")
        dt = request.form.get("dt")
        tm = Reg.query.filter_by(id=id).first()
        if(tm == None):
            return '<h1> The Student is not in the system kindly retype and make sure the input you provided is right</h1>'
        else:
            if dt[5:7] == '11':
                # print("tm.october_invoice")
                tm.november = True
                # print("I am here")
                tm.november_invoice += int(amount)
                db.session.commit()
                inv = Reg.query.all()
                return render_template("reciept.html", inv=inv)
            elif dt[5:7] == '12':
                tm.december = True
                tm.december_invoice += int(amount)
                db.session.commit()
                inv = Reg.query.all()
                return render_template("reciept.html", inv=inv)
            elif dt[5:7] == '01':
                tm.january = True
                tm.january_invoice += int(amount)
                db.session.commit()
                inv = Reg.query.all()
                return render_template("reciept.html", inv=inv)

            elif dt[5:7] == '02':
                tm.february = True
                tm.february_invoice += int(amount)
                inv=Reg.query.all()
                return render_template("reciept.html",inv=inv)

            elif dt[5:7]=='03':
                tm.march=True
                tm.march_invoice+=int(amount)
                inv=Reg.query.all()
                return render_template("reciept.html",inv=inv)

            elif dt[5:7]=='04':
                tm.aprill=True
                tm.aprill_invoice+=int(amount)
                inv=Reg.query.all()
                return render_template("reciept.html",inv=inv)

            elif dt[5:7]=='05':
                tm.may=True
                tm.may_invoice+=int(amount)
                inv=Reg.query.all()
                return render_template("reciept.html",inv=inv)

            elif dt[5:7]=='06':
                tm.june=True
                tm.june_invoice+=int(amount)
                inv=Reg.query.all()
                return render_template("reciept.html",inv=inv)
            elif dt[5:7]=='07':
                tm.july=True
                tm.july_invoice+=int(amount)
                inv=Reg.query.all()
                return render_template("reciept.html",inv=inv)
            elif dt[5:7]=='08':
                tm.august=True
                tm.august_invoice+=int(amount)
                inv=Reg.query.all()
                return render_template("reciept.html",inv=inv)
            elif dt[5:7]=='09':
                tm.september=True
                tm.september_invoice+=int(amount)
                inv=Reg.query.all()
                return render_template("reciept.html",inv=inv)
            elif dt[5:7]=='10':
                tm.october=True
                tm.october_invoice+=int(amount)
                inv=Reg.query.all()
                return render_template("reciept.html",inv=inv)
            else:
                return 'The developer is still working on the application'

    else:
        stu=Pathfinder.query.all()
        return render_template("index.html",stu=stu)

@app.route("/delete", methods=["POST"])
def delete():
	if not session.get('logged_in'):
		return render_template('login.html')
	id = request.form.get("id2")
	tmp = Pathfinder.query.filter_by(id=id).first()
	db.session.delete(tmp)
	db.session.commit()
	t= Reg.query.filter_by(id=id).first()
	db.session.delete(t)
	db.session.commit()
	return redirect("/")

@app.route("/students",methods=["GET"])
def show():
	stu=Pathfinder.query.all()
	return render_template("shows.html",stu=stu)

@app.route("/payments",methods=["GET"])
def invoice():
	inv=Reg.query.all()
	return render_template("reciept.html",inv=inv)


if __name__ == "__main__":
    app.secret_key = "something random"
    app.run(debug=True)

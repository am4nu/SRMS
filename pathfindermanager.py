#Python 3.6 Code
import os
import datetime
from flask import Flask, redirect
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "pf.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
class Pathfinder(db.Model):
	id=db.Column(db.String(100),nullable=False,primary_key=True,unique=True,autoincrement=False)
	firstname=db.Column(db.String(80),nullable=False)
	lastname=db.Column(db.String(80),nullable=False)
	middlename=db.Column(db.String(80),nullable=True)
	addr=db.Column(db.String(80),nullable=False)
	school=db.Column(db.String(80),nullable=True)
	fname=db.Column(db.String(80),nullable=True)
	phone=db.Column(db.Integer,nullable=True)
	batch=db.Column(db.String(4),nullable=True)
	dateAdd=db.Column(db.String(10),nullable=False)
	optradio=db.Column(db.String(10),nullable=False)
	def __repr__(self):
		return "<ID & Name  {} >".format(str(self.id))
		
class Reg(db.Model):
	id=db.Column(db.String(100),nullable=False,primary_key=True,unique=True,autoincrement=False)
	firstname=db.Column(db.String(80),nullable=False)
	lastname=db.Column(db.String(80),nullable=False)
	january=db.Column(db.Boolean,   default=False)
	february=db.Column(db.Boolean,   default=False)
	march=db.Column(db.Boolean,   default=False)
	aprill=db.Column(db.Boolean,   default=False)
	may=db.Column(db.Boolean,   default=False)
	june=db.Column(db.Boolean,   default=False)
	july=db.Column(db.Boolean,   default=False)
	august=db.Column(db.Boolean,   default=False)
	september=db.Column(db.Boolean,   default=False)
	october=db.Column(db.Boolean,   default=False)
	november=db.Column(db.Boolean,   default=False)
	december=db.Column(db.Boolean,nullable=False,default=False)
	january_invoice=db.Column(db.Integer,   default=False)
	february_invoice=db.Column(db.Integer,   default=False)
	march_invoice=db.Column(db.Integer,   default=False)
	aprill_invoice=db.Column(db.Integer,   default=False)
	may_invoice=db.Column(db.Integer,   default=False)
	june_invoice=db.Column(db.Integer,   default=False)
	july_invoice=db.Column(db.Integer,   default=False)
	august_invoice=db.Column(db.Integer,   default=False)
	september_invoice=db.Column(db.Integer,   default=False)
	october_invoice=db.Column(db.Integer,   default=False)
	november_invoice=db.Column(db.Integer,   default=False)
	december_invoice=db.Column(db.Integer,   default=False)
	def __repr__(self):
		return "<ID {} >".format(str(self.id))
		
@app.route("/reg",methods=["POST","GET"])
def home():
	if request.method=="POST":
		fn=request.form.get("firstname")
		ln=request.form.get("lastname")
		mn=request.form.get("middlename")
		addr=request.form.get("addr")
		school=request.form.get("school")
		fname=request.form.get("fname")
		phone=request.form.get("phone")
		batch=request.form.get("batch")
		dateAdd=request.form.get("dateAdd")
		optradio=request.form.get("optradio")
		pathfinder=Pathfinder(id=fn+ln+str(phone)+dateAdd,firstname=fn,lastname=ln,middlename=mn,addr=addr,phone=phone,school=school,fname=fname,batch=batch,dateAdd=dateAdd,optradio=optradio)
		pt= Pathfinder.query.filter_by(id=fn+ln+str(phone)+str(dateAdd)).all() #queries for that particular record in the db
		#print(pt)
		if(len(pt)==0): #if the record is not alrdy there it add's it
			db.session.add(pathfinder)
			db.session.commit()
			temp=Reg(id=fn+ln+str(phone)+dateAdd,firstname=fn,lastname=ln)
			db.session.add(temp)
			db.session.commit()
			return redirect("/show")
		else:
			return '<h1>Error Record with same FirstName Lastname Phone and DOB exists</h1>'
	else:
		return render_template("index.html")
	
	
@app.route("/pay",methods=["POST","GET"])
def pay():
	if request.method=="POST":
		fn=request.form.get("firstname")
		ln=request.form.get("lastname")
		phone=request.form.get("phone")
		dob=request.form.get("dob")
		inv=request.form.get("invoice")
		now = datetime.datetime.now()
		tm= Pathfinder.query.filter_by(id=fn+ln+str(phone)+str(dob)).all()
		if(len(tm)==0):
			return '<h1> The Student is not in the system kindly retype and make sure the input you provided is right</h1>'
		if now.month==1:
			print("i am here")
			temp=Reg(october_invoice=inv,october=True)
			db.session.add(temp)
			db.session.commit()
			return '<h1>The student paid, Congrats!</h1>'
	
	else:	
		return render_template("pay.html")
@app.route("/show",methods=["GET"])
def show():
	stu=Pathfinder.query.all()
	return render_template("shows.html",stu=stu)
  
if __name__ == "__main__":
    app.run(debug=True)
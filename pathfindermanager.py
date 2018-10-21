import os
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
pfile_dir= os.path.dirname(os.path.abspath(__file__))
db_file="sqlite:///{}".format(os.path.join(pfile_dir,"pathfinder.db"))
app = Flask(__name__)
app.config["SQLAlCHEMY_DATABASE_URI"] = db_file
db=SQLAlchemy(app)

@app.route("/mgmt",methods=["POST","GET"])
def home():
	if request.form:
		id=request.form.get("id")
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
		pathfinder=Pathfinder(id=id,firstname=fn,lastname=ln,middlename=mn,addr=addr,school=school,fname=fname,batch=batch,dateAdd=dateAdd,optradio=optradio)
		db.session.add(pathfinder)
		db.session.commit()
	return render_template("index.html")
		
		
	return render_template("index.html")

class Pathfinder(db.Model):
	id=db.Column(db.Integer,nullable=False,primary_key=True)
	firstname=db.Column(db.String(80),nullable=False)
	lastname=db.Column(db.String(80),nullable=False)
	middlename=db.Column(db.String(80),nullable=True)
	addr=db.Column(db.String(80),nullable=False)
	school=db.Column(db.String(80),nullable=True)
	fname=db.Column(db.String(80),nullable=True)
	phone=db.Column(db.String(80),nullable=True,)
	batch=db.Column(db.String(4),nullable=True)
	dateAdd=db.Column(db.String(10),nullable=False)
	optradio=db.Column(db.String(10),nullable=False)
	def __repr__(Self):
		return "<Name & Phone {} >".format(self.firstname+self.lastname+self.phone)
	
	
  
if __name__ == "__main__":
    app.run(debug=True)
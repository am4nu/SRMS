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

@app.route("/",methods=["POST","GET"])
def home():
	if request.form:
		print(request.form)
	return render_template("home.html")
  
if __name__ == "__main__":
    app.run(debug=True)
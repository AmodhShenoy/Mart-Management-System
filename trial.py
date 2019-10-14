from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
db = MySQL(app)

app.config['MYSQL_USER'] = 'dbms'
app.config['MYSQL_PASSWORD'] = 'dbmsproject'
app.config['MYSQL_DB'] = 'dbms'
app.config['MYSQL_HOST'] = 'localhost'


#login
@app.route('/',methods=['GET','POST'])
def login():
	cur = db.connection.cursor()
	cur.execute("SELECT * from EMPLOYEE;")
	l = cur.fetchall()
	for i in l:
		print(l)
	return "DOne"

if __name__=='__main__':
	app.run()

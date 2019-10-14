from flask import Flask, render_template, request
from flask_mysqldb import MySQL

db = MySQL()
app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'iwannaknow101'
app.config['MYSQL_DB'] = 'dbms'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 5000


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
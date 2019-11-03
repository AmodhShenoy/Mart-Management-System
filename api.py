from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
db = MySQL(app)

app.secret_key = 'dbms'
app.config['MYSQL_USER'] = 'dbmsuser'
app.config['MYSQL_PASSWORD'] = 'pwd'
app.config['MYSQL_DB'] = 'dbms'
app.config['MYSQL_HOST'] = 'localhost'

#login
@app.route('/',methods=['GET','POST'])
def login():
	if request.method=='GET':
		return render_template('land.html')
	else:
		cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
		username = request.form.get("username")
		cur.execute('SELECT * FROM EMPLOYEE WHERE Username = %s',(str(username),))
		l = cur.fetchone()
		if not l:
			return render_template('land.html', msg = 'Invalid Username')

		pwd = request.form.get("pwd")
		cur.execute('SELECT EmpID,EmpPassword FROM EMPLOYEE WHERE Username = %s',(str(username),))

		row = cur.fetchone()
		if row and pwd == row['EmpPassword']:
			session['loggedin'] = True
			session['id'] = row['EmpID']
			session['username'] = str(username)
			print("hey")
			print(session)
			return render_template('land.html', msg = 'Hello')
		else:
			return render_template('land.html', msg = 'Invalid Password')


	# db = MySQLdb.connect("localhost","root",'iwannaknow101','trial')
	# cursor = db.cursor()
	# cursor.execute('INSERT INTO ITEMS VALUES (22,"mastitem",99);')
	# db.commit()
	# db.close()
	# return "SUCCESS"

# #creating a new item
# @app.route('/items/new')
# pass

# #modifying item details
# @app.route('/items/modify')
# pass

# #adding a sale
# @app.route('/inventory/sell')
# pass

# #adding items to the inventory
# @app.route('/inventory/store')
# pass

# #removing items from the inventory for unknown reasons
# @app.route('inventory/items/remove')
# pass

# #adding inventory to store
# @app.route('/inventory/add')
# pass

# #remove items from inventory
# @app.route('/inventory/remove')
# pass

# #delete inventory as a whole
# @app.route('/inventory/delete')
# pass

# #add a new store
# @app.route('/store/add')
# pass

# #remove a store
# @app.route('/store/remove')
# pass

# #modify the store details
# @app.route('/store/modify')
# pass

if __name__ == '__main__':
	app.run(debug=True)

from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from flask_session import Session

db = MySQL()
app = Flask(__name__)
db = MySQL(app)

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
		username = request.form.get('username')
		pwd = request.form.get('pwd')
		cur = db.connection.cursor()
		cur.execute("SELECT * from EMPLOYEE;")
		db.connection.commit()
		emps = cur.fetchall()
		for emp in emps:
			if emp[2]==pwd and emp[4]==username:
				session['EmpID'] = emp[0]
				session['ShopID'] = emp[3]
				cur.execute("SELECT * FROM MANAGES;")
				db.connection.commit()
				checks = cur.fetchall()
				session['Manager'] = False
				for i in checks:
					if i[0]==emp[0] and i[1]==emp[3]:
						session['Manager'] = True
						break
				cur.close()
				return "Logged in"
		return "Error"


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
	app.secret_key = "abc"
	app.run(debug=True)

from flask import Flask, render_template, request
from flask_mysqldb import MySQL

db = MySQL()
app = Flask(__name__)
db = MySQL(app)

app.config['MYSQL_USER'] = 'dbms'
app.config['MYSQL_PASSWORD'] = 'dbmsproject'
app.config['MYSQL_DB'] = 'dbms'
app.config['MYSQL_HOST'] = 'localhost'

#login
@app.route('/',methods=['GET','POST'])
def login():
	if request.method=='GET':
		return render_template('templates/login.html')
	else:
		username = request.form.get('uname')
		pwd = reqeust.form.get('pwd')
		cur = db.connection.cursor()
		cur.execute("SELECT EmpID from EMPLOYEE WHERE Username='%s' AND EmpPassword='%s';".format(username,pwd))
		db.commit()
		l = cur.fetchall()
		if len(l)==1:
			return l[0]
	cur = db.connection.cursor()


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

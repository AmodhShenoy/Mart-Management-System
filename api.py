from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import fbprophet
import pandas as pd
from datetime import date,timedelta,datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import time
import io

app = Flask(__name__)
db = MySQL(app)

app.secret_key = 'dbms'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vithik13&'
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
		cur.execute('SELECT ShopID,EmpID,EmpPassword FROM EMPLOYEE WHERE Username = %s',(str(username),))

		row = cur.fetchone()
		if row and pwd == row['EmpPassword']:
			session['loggedin'] = True
			session['empid'] = row['EmpID']
			session['shopid'] = row['ShopID']
			session['username'] = str(username)
			cur.execute('SELECT * FROM MANAGES WHERE EmpID='+str(session['empid'])+' AND ShopID='+str(session['shopid'])+';')
			a = cur.fetchone()
			if a:
				session['manager'] = True
				return redirect(url_for('manager_add_item'))
			else:
				session['manager'] = False
				return redirect(url_for('index'))
		else:
			return render_template('land.html', msg = 'Invalid Password')
		cur.close()

#Index page for employee
@app.route('/index',methods=['GET','POST'])
def index():
	if request.method=='GET':
		cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
		query = "SELECT * FROM  INVENTORY WHERE ShopID = " + str(session['shopid'])
		cur.execute(query)
		items = cur.fetchall()
		query = "SELECT * FROM ITEMS"
		cur.execute(query)
		item_det = cur.fetchall()
		item_names = {}
		for x in item_det:
			item_names[x['ItemID']] = x['Name']
		return render_template('index.html', items = items, item_names = item_names)
	if request.method=='POST':
		item_id = request.form.get("item_id")
		item_quantity = request.form.get("item_quantity")
		cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
		query = "SELECT Units FROM  INVENTORY WHERE ShopID = " + str(session['shopid']) + " AND ItemID = " + str(item_id)
		cur.execute(query)
		old_value = cur.fetchone()['Units']
		new_value = int(old_value) - int(item_quantity)
		query = "UPDATE INVENTORY SET Units = " + str(new_value) + " WHERE ShopID = " + str(session['shopid']) + " AND ItemID = " +str(item_id)
		cur.execute(query)
		query = "INSERT INTO SALES VALUES(" + str(session['shopid']) + "," + str(item_id) + "," + str(item_quantity) + ",CURRENT_TIME())" 
		cur.execute(query) 
		cur.close()
		db.connection.commit()
		return redirect(url_for('index'))

#For adding item quantity
@app.route('/add',methods=['POST'])
def add():
	if request.method=='POST':
		item_id = request.form.get("item_id")
		item_quantity = request.form.get("item_quantity")
		cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
		query = "SELECT Units FROM  INVENTORY WHERE ShopID = " + str(session['shopid']) + " AND ItemID = " + str(item_id)
		cur.execute(query)
		old_value = cur.fetchone()['Units']
		new_value = int(old_value) + int(item_quantity)
		query = "UPDATE INVENTORY SET Units = " + str(new_value) + " WHERE ShopID = " + str(session['shopid']) + " AND ItemID = " +str(item_id)
		cur.execute(query)
		cur.close()
		db.connection.commit()
		return redirect(url_for('index'))

#Adding new item
@app.route('/manager_add_item',methods=['GET','POST'])
def manager_add_item():
	if request.method=='GET':
		cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
		query = "SELECT * FROM ITEMS"
		cur.execute(query)
		items = cur.fetchall()
		return render_template('manager_add_item.html', items = items)
	if request.method=='POST':
		item_id = request.form.get("item_id")
		item_quantity = request.form.get("item_quantity")
		cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
		query = "INSERT INTO INVENTORY VALUES(" + str(session['shopid']) + "," +  str(item_id) + "," + str(item_quantity) + ")"
		cur.execute(query)
		cur.close()
		db.connection.commit()
		return redirect(url_for('index'))




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

@app.route('/predict/<shopid>',methods=['GET'])
def predict(shopid):
	cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
	cur.execute('SELECT ItemID,Quantity,SaleDate FROM SALES WHERE ShopID='+shopid+';')
	l = cur.fetchall()
	sales = []
	for i in l:
		sales.append(i.values())

	ll = []
	today = datetime.strptime('2019-08-14','%Y-%m-%d')
	# today = date.today()
	for i in range(1,8):
		da = today + timedelta(days=i)
		ll.append(str(da))
	data = pd.DataFrame(sales,columns=['ItemID','y','ds'])
	prediction = pd.DataFrame(columns=list(data['ItemID'].unique())+['y'],index=ll)
	for i in prediction.columns:
		prediction[i]=0
	print(prediction)
	for item in data['ItemID'].unique():
		d = data[data.ItemID==item].drop(['ItemID'],axis=1)
		model = fbprophet.Prophet()
		model.fit(d)
		START_DATE = datetime.strptime('2019-08-10','%Y-%m-%d')
		today = datetime.strptime('2019-08-14','%Y-%m-%d')
		per = today - START_DATE
		p = model.make_future_dataframe(periods=per.days+8)
		fc = model.predict(p)
		for i in fc['ds']:
			if str(i) in prediction.index:
				prediction.loc[str(i)][item] += int(round(fc[fc.ds==i]['yhat']))

		for i in prediction.index:
			sum = 0
			for j in prediction.columns:
				if j!='y':
					sum+=prediction.loc[i][j]
			prediction.loc[i]['y'] = sum
	
	x = list(prediction.index)
	for i in range(len(x)):
		x[i] = datetime.strptime(x[i][:10],'%Y-%m-%d')
	y = prediction['y']

	plt.plot(x,y)
	plt.tight_layout()
	plt.xlabel('Dates')
	plt.ylabel('No. of sales predicted')
	plt.savefig('static/images/foo.png')
	print("PLOT SAVED")
	time.sleep(2)
	print(prediction)
	return render_template('timeseries.html', tables = [prediction.to_html(classes='data')],titles=prediction.columns.values)


if __name__ == '__main__':
	app.run(debug=True)

from flask import Flask
app = Flask(__name__)

#login
@app.route('/')
pass

#creating a new item
@app.route('/items/new')
pass

#modifying item details
@app.route('/items/modify')
pass

#adding a sale
@app.route('/inventory/sell')
pass

#adding items to the inventory
@app.route('/inventory/store')
pass

#removing items from the inventory for unknown reasons
@app.route('inventory/items/remove')
pass

#adding inventory to store
@app.route('/inventory/add')
pass

#remove items from inventory
@app.route('/inventory/remove')
pass

#delete inventory as a whole
@app.route('/inventory/delete')
pass

#add a new store
@app.route('/store/add')
pass

#remove a store
@app.route('/store/remove')
pass

#modify the store details
@app.route('/store/modify')
pass

if __name__ == '__main__':
	app.run(debug=True)
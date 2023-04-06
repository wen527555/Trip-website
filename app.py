from flask import Flask
from flask import *
from flask import render_template
from flask import make_response 
from flask import jsonify 
from flask_jwt_extended import JWTManager
from api.booking import booking_blueprint
from api.order import order_blueprint
from api.user import user_blueprint
from api.index import index_blueprint


app=Flask(__name__)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 604800  # JWT token 有效期為七天

jwt = JWTManager(app)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


app.register_blueprint(booking_blueprint)
app.register_blueprint(order_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(index_blueprint)



app.run(host='0.0.0.0',port=3000,debug=True)




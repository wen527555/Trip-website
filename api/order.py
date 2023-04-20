
from flask import request
from flask import *
from flask import render_template
from flask import make_response 
from flask import session
from mysql.connector import pooling
from flask import jsonify 
from flask_jwt_extended import  jwt_required, get_jwt_identity
import time
import random
import string
import requests
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
PARTNER_KEY = os.getenv('PARTNER_KEY')



connection_pooling=pooling.MySQLConnectionPool(
                                            pool_name="mypool",
                                            pool_size=5,
                                            pool_reset_session='True',
                                            host='localhost',
                                            database=DATABASE_NAME,
                                            user=DB_USER,
                                            password=DB_PASSWORD)

                            

order_blueprint = Blueprint('order_blueprint', __name__)

#建立新的付款訂單
@order_blueprint.route('/api/orders',methods=['POST'])
@jwt_required()
def order_post():
    try:
        order_data=request.json
        prime=order_data["prime"]
        orders=order_data["orders"]
        trip=orders["trip"][0]
        totalPrice=trip["price"]     
        attraction=trip["attraction"]
        contact=orders["contact"]
        contactName=contact["name"]
        contactEmail=contact["email"]
        contactPhone=contact["phone"]
        user_email=get_jwt_identity()
        if not user_email:
            return jsonify({"error":True,"message":"未登入，拒絕存取"}),403
        # 進行 TapPay 付款程序
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            orderNumber=time.strftime("%Y%m%d%H%M%S")+''.join(random.choices(string.ascii_letters + string.digits, k=6))
            mycursor.execute("SELECT id FROM user WHERE email=%s",[user_email])
            result=mycursor.fetchone()       
            user_id=result["id"]
            mycursor.execute("INSERT INTO orders (order_number, prime, attraction_id, attraction_name, attraction_address, attraction_images, date, time, price, contact_name, contact_email, contact_phone,user_id ,payment_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)", (orderNumber,prime ,attraction["id"], attraction["name"], attraction["address"], attraction["image"], trip["date"], trip["time"], totalPrice, contactName, contactEmail, contactPhone,user_id ,'未付款'))
            connection_object.commit()
            response = requests.post('https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime',
                                headers={
                                    'Content-Type': 'application/json',
                                    'x-api-key':PARTNER_KEY
                                },
                                json={
                                    'partner_key': PARTNER_KEY,
                                    "merchant_id": "wen527555_ESUN",
                                    'prime': prime,
                                    'amount': totalPrice,
                                    'currency': 'TWD',
                                    'details': 'Trip Order',
                                    'cardholder': {
                                        'phone_number':contactPhone,
                                        'name': contactName,
                                        'email': contactEmail
                                    }
                                })
            # 付款成功
            if  response.status_code == 200 and response.json()['status'] == 0:
                mycursor.execute("UPDATE orders SET payment_status='已付款' WHERE order_number=%s ",(orderNumber,))
                connection_object.commit()
                mycursor.execute("SELECT id FROM user WHERE email=%s",[user_email])
                result=mycursor.fetchone()       
                user_id=result["id"]
                mycursor.execute("DELETE FROM booking WHERE user_id=%s",[user_id])
                connection_object.commit()
            # 回傳訂單編號和付款狀態
                return jsonify({
                    'data': {
                        'number': orderNumber,
                        'payment': {
                            'status': 0,
                            'message': '付款成功'
                        }
                    }
                }),200
            # 付款失敗
            else:
                return jsonify({
                    'error':True,
                    'data': {
                        'number': orderNumber,
                        'payment': {
                            'status': -1,
                            'message': '付款失敗，請檢查付款資訊是否正確'
                        }
                    }
                }),400



    except Exception as e:
        return jsonify({"error": True, "message": str(e)}),500

    finally:
        connection_object.close()


#根據訂單編號取得訂單資訊
@order_blueprint.route('/api/order/<orderNumber>',methods=['GET'])
@jwt_required()
def order_get(orderNumber):
    try:
        user_email=get_jwt_identity()
        if not user_email:
            return jsonify({"error":True,"message":"未登入，拒絕存取"}),403
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            mycursor.execute("SELECT * FROM orders WHERE order_number=%s ",(orderNumber,))
            order_data=mycursor.fetchone()
            if order_data:       
                contact={
                    "name":order_data["contact_name"],
                    "email":order_data["contact_email"],
                    "phone":order_data["contact_phone"],
                }
                attraction={
                    "id":order_data["attraction_id"],
                    "name":order_data["attraction_name"],
                    "address":order_data["attraction_address"],
                    "image":order_data["attraction_images"],
                }
                order_info={
                    "number":orderNumber,
                    "price":order_data["price"],
                    "trip":{
                        "attraction":attraction,
                        "date":order_data["date"],
                        "time":order_data["time"],
                    },
                    "contact":contact
                    ,
                    "status":1                     
                }
                return jsonify({"data":order_info}),200

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}),500

    finally:
        connection_object.close()



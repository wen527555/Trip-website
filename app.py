
import flask
from flask import Flask
from flask import request
from flask import *
from flask import render_template
from flask import make_response 
from flask import session
from mysql.connector import pooling
from flask import jsonify 
import math
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
# import requests
import time
import random
import string
import requests


connection_pooling=pooling.MySQLConnectionPool(
                                            pool_name="mypool",
                                            pool_size=5,
                                            pool_reset_session='True',
                                            host='localhost',
                                            database='taipei_day_trip',
                                            user='root',
                                            password='wh1999ne123')

app=Flask(__name__)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # JWT 密鑰，需自行替換
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

@app.route("/api/attractions", methods=['GET'])
def get_attractions():
    try:
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            page=request.args.get("page",0,type=int)   
            keyword=request.args.get("keyword",'')
            per_page=12
            mycursor.execute("SELECT COUNT(`id`) FROM attractions")
            total_data=mycursor.fetchone()
            total_data=total_data['COUNT(`id`)']
            total_page=math.floor(total_data/12)
            next_page=int(page +1) 
            if keyword != None:
                mycursor.execute("SELECT * FROM attractions WHERE category=%s or LOCATE(%s,`name`) LIMIT %s,12",[keyword,keyword,page*per_page])
            else:
                mycursor.execute("SELECT * FROM attractions LIMIT %s,12",[page*per_page])
                
            results=mycursor.fetchall()
            if len(results)<12:
                next_page = None
            data_all=[]
            for result in results:
                new_images=[]
                images=result["images"].split(",")
                for image in images:
                    new_images.append(image)

                data={
                "id":result["id"],
                "name":result["name"],
                "category":result["category"],
                "description":result["description"],
                "address":result["address"],
                "transport":result["transport"],
                "mrt":result["mrt"],
                "lat":result["lat"],
                "lng":result["lng"],
                "images":new_images           
                }
                data_all.append(data)

            if total_page >= page:
                attractions={
                        "nextPage":next_page,
                        "data":data_all
                                    }
                ans= jsonify(attractions)
            else:
                error={
                    "error":True,
                    "message":"無此頁面"
                }
                ans= jsonify(error)
            return ans
    except Exception as e:
        return {"error": True, "message": str(e)},500

    finally:
        connection_object.close()   

@app.route("/api/attraction/<attractionId>", methods=['GET'])
def get_attraction(attractionId):
    try:
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            mycursor.execute("SELECT * FROM attractions WHERE id=%s ",(attractionId,))
            results=mycursor.fetchone()
            if not results:
                return{"error":True,"message":"景點編號不正確"}
            new_images=[]
            images=results["images"].split(",")
            for image in images:
                new_images.append(image)

            data={
                "id":results["id"],
                "name":results["name"],
                "category":results["category"],
                "description":results["description"],
                "address":results["address"],
                "transport":results["transport"],
                "mrt":results["mrt"],
                "lat":results["lat"],
                "lng":results["lng"],
                "images":new_images
            }
            #回傳JSON格式的景點資料
            return jsonify({"data":data})

    except Exception as e:
        return {"error": True, "message": str(e)}

    finally:
        connection_object.close()

@app.route("/api/categories", methods=['GET'])
def get_categories():
    try:
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            mycursor.execute("SELECT DISTINCT category FROM attractions")
            results=mycursor.fetchall()
            categories=[result['category'] for result in results ]
            return {"data":categories}
    except Exception as e:
        return {"error": True, "message": str(e)},500

    finally:
        connection_object.close()



# 會員註冊
@app.route('/api/user',methods=['POST'])
def register():
    try:
        #檢查使用者名稱是否存在
        data=request.json
        print(data)
        name=data["name"]
        password=data["password"]
        email=data["email"]
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            if not email or not password or not name:
                return {"error":True,"message":"所有欄位皆須填寫，請勿空白"}
            mycursor.execute("SELECT email FROM user WHERE email=%s",[email,])
            user=mycursor.fetchone()
            if not user :
                hashed_password = generate_password_hash(password, method='sha256')
                mycursor.execute("INSERT INTO user (name,email,password) VALUES( %s, %s, %s)",[name,email,hashed_password])
                connection_object.commit()
                user=mycursor.fetchone()
                response= jsonify({"OK":True,"data":user,"message":"註冊成功！"}),200 
                return response
            else:
                return{"error":True,"message":"此email已註冊過，請登入"},400

            

    except Exception as e:
        return {"error": True, "message": str(e)},500

    finally:
        connection_object.close()

#會員登入狀態檢查
@app.route('/api/user/auth',methods=['GET'])
@jwt_required()
def auth_get():
    try:
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            email=get_jwt_identity()
            if email:
                mycursor.execute("SELECT id,name,email FROM user WHERE email=%s",[email])
                user=mycursor.fetchone()
                print("user")
                response= jsonify({"data":user})
                return response
            else:
                return jsonify({"error":True,"message":"尚未登入"}),403

    except Exception as e:
            return {"error": True, "message": str(e)},500

    finally:
        connection_object.close()


@app.route('/api/user/auth',methods=['PUT','DELETE'])

def auth():
    try:
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            # 會員登入
            if request.method=='PUT':
                data=request.get_json()
                print(data)
                password=data["password"]
                email=data["email"]
                if not email or not password:
                    return {"error":True,"message":"請輸入完整的email及密碼"}
                mycursor.execute("SELECT * FROM user WHERE email=%s",[email])
                results=mycursor.fetchone()
                if not results:
                    return {"error":True,"message":"無此使用者，請先註冊"}
                elif not check_password_hash(results["password"],password):
                    return {"error":True,"message":"密碼錯誤"}
                elif results:
                    access_token=create_access_token(identity=email)
                    response=make_response({"ok":True})
                    response.set_cookie("access_token", access_token, secure=False)
                    return response
                    

            # 會員登出
            elif request.method=='DELETE':
                response=make_response({"ok":True})
                response.delete_cookie("access_token")
                return response

    except Exception as e:
        return {"error": True, "message": str(e)},500

    finally:
        connection_object.close()

#預定行程

#取得尚位確認下單的預定行程
@app.route('/api/booking',methods=['GET'])
@jwt_required()
def booking_get():
    try:
        user_email=get_jwt_identity()
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            if user_email:      
                mycursor.execute("SELECT id,name FROM user WHERE email=%s",[user_email])
                result=mycursor.fetchone()      
                user_id=result["id"]
                mycursor.execute("SELECT booking.id,booking.date,booking.time,booking.price, attractions.id,attractions.name,attractions.address,attractions.images FROM booking JOIN attractions ON booking.attraction_id=attractions.id WHERE booking.user_id=%s",[user_id])
                booking_data=mycursor.fetchone()
                if booking_data:
                    new_images=[]
                    images=booking_data["images"].split(",")
                    for image in images:
                        new_images.append(image)         
                    date=booking_data["date"].strftime('%Y-%-m-%-d')
                    price=int(booking_data["price"])
                    booking_info={
                        "username":result["name"],
                        "date":date,
                        "time":booking_data["time"],
                        "price":price,
                        "attraction":{
                        "id":booking_data["id"],    
                        "name":booking_data["name"],
                        "address":booking_data["address"],
                        "image":new_images,
                        }                        
                    }
                    # print(booking_info)
                    return jsonify({"data":booking_info}),200      
                else:
                    return jsonify({"data":None,"message":"沒有預定的行程"})           

            else:
                response={
                "error":True,
                "message":"未登入，拒絕存取"
            } 
                return jsonify(response),403

    except Exception as e:
        return {"error": True, "message": str(e)},500

    finally:
        mycursor.close()
        connection_object.close()

#建立新的預定行程
@app.route('/api/booking',methods=['POST'])
@jwt_required()
def booking_post():
    try:
        user_email=get_jwt_identity()
        data=request.json
        date=data["date"]
        time=data["time"]
        price=data["price"]
        attractionId=data["attractionId"]
        print(attractionId,date,time,price, user_email)
        if not date or not time or not price or not attractionId :
            return jsonify({"error":True,"message":"所有欄位皆須填寫，請勿空白"}),400
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:          
            if user_email:      
                mycursor.execute("SELECT id FROM user WHERE email=%s",[user_email])
                result=mycursor.fetchone()       
                user_id=result["id"]
                #檢查是否有預定的行程
                mycursor.execute("SELECT user_id FROM booking WHERE user_id=%s",[user_id])
                pre_booking=mycursor.fetchone() 
                if pre_booking:
                    mycursor.execute("DELETE FROM booking WHERE user_id=%s", [pre_booking["user_id"]])
                    connection_object.commit()                   
                mycursor.execute("INSERT INTO booking (user_id, attraction_id, date, time, price) VALUES (%s, %s, %s, %s, %s)", [user_id, attractionId, date, time, price])

                connection_object.commit()
                data={
                    "attractionId":attractionId,
                    "date":date,
                    "time":time,
                    "price":price,
                }
                print(data)
                return jsonify({"data":data}),200

            else:
                response={
                "error":True,
                "message":"未登入，拒絕存取"
            } 
                return jsonify(response),403

    except Exception as e:
        return {"error": True, "message": str(e)},500

    finally:
        connection_object.close()

#刪除目前預定的行程
@app.route('/api/booking',methods=['DELETE'])
@jwt_required()
def booking_delete():
    try:
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            user_email=get_jwt_identity()
            if user_email:
                #找出該使用者的預定行程
                mycursor.execute("SELECT id FROM user WHERE email=%s",[user_email])
                result=mycursor.fetchone()       
                user_id=result["id"]
                #檢查是否有預定的行程
                mycursor.execute("SELECT id FROM booking WHERE user_id=%s",[user_id])
                booking_data=mycursor.fetchone()
                if not booking_data:
                    return jsonify({"error":True,"message":"沒有預定的行程"}),400
                else:
                    mycursor.execute("DELETE FROM booking WHERE user_id=%s",[user_id])
                    connection_object.commit()
                    return jsonify({"ok":True}),200
                                        
            else:
                response={
                "error":True,
                "message":"未登入，拒絕存取"
            } 
                return jsonify(response),403

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}),500

    finally:
        connection_object.close()

#建立新的付款訂單
@app.route('/api/orders',methods=['POST'])
@jwt_required()
def order_post():
    try:
        order_data=request.json
        print(order_data)
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
            print(orderNumber)
            mycursor.execute("INSERT INTO orders (order_number, prime, attraction_id, attraction_name, attraction_address, attraction_images, date, time, price, contact_name, contact_email, contact_phone, payment_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (orderNumber,prime ,attraction["id"], attraction["name"], attraction["address"], attraction["image"], trip["date"], trip["time"], totalPrice, contactName, contactEmail, contactPhone, '未付款'))
            connection_object.commit()
            response = requests.post('https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime',
                                headers={
                                    'Content-Type': 'application/json',
                                    'x-api-key': 'partner_HLMcv6auy331Uwg7BMCJHWDEtIL0OT4DsGPKrV7Ea0hB9HcYJHHke8mI'
                                },
                                json={
                                    'partner_key': 'partner_HLMcv6auy331Uwg7BMCJHWDEtIL0OT4DsGPKrV7Ea0hB9HcYJHHke8mI',
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
                # mycursor.execute("SELECT id FROM user WHERE email=%s",[user_email])
                # result=mycursor.fetchone()       
                # user_id=result["id"]
                # mycursor.execute("DELETE FROM booking WHERE user_id=%s",[user_id])
                # connection_object.commit()
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
@app.route('/api/orders/<orderNumber>',methods=['GET'])
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
                new_images=[]
                images=order_data["images"].split(",")
                for image in images:
                    new_images.append(image)         
                date=order_data["date"].strftime('%Y-%-m-%-d')
                price=int(order_data["price"])
                contact={
                    "name":order_data["contact_name"],
                    "email":order_data["contact_email"],
                    "phone":order_data["contact_phone "],
                }
                attraction={
                    "id":order_data["attraction_id"],
                    "name":order_data["attraction_name"],
                    "address":order_data["attraction_address"],
                    "image":new_images,
                }
                order_info={
                    "number":orderNumber,
                    "price":price,
                    "trip":{
                        "attraction":attraction,
                        "date":date,
                        "time":order_data["time"],
                    },
                    "contact":contact
                    ,
                    "status":1                     
                }
                # print(booking_info)
                return jsonify({"data":order_info}),200

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}),500

    finally:
        connection_object.close()

app.run(host='0.0.0.0',port=3000,debug=True)




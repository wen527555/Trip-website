from flask import request
from flask import *
from flask import render_template
from flask import make_response 
from flask import session
from flask import jsonify 
from flask_jwt_extended import jwt_required, get_jwt_identity
from mysql.connector import pooling
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

connection_pooling=pooling.MySQLConnectionPool(
                                            pool_name="mypool",
                                            pool_size=5,
                                            pool_reset_session='True',
                                            host='localhost',
                                            database=DATABASE_NAME,
                                            user=DB_USER,
                                            password=DB_PASSWORD)

booking_blueprint = Blueprint('booking_blueprint', __name__)

#取得尚位確認下單的預定行程
@booking_blueprint.route('/api/booking',methods=['GET'])
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
@booking_blueprint.route('/api/booking',methods=['POST'])
@jwt_required()
def booking_post():
    try:
        user_email=get_jwt_identity()
        data=request.json
        date=data["date"]
        time=data["time"]
        price=data["price"]
        attractionId=data["attractionId"]
        if not date or not time or not price or not attractionId :
            return jsonify({"error":True,"message":"所有欄位皆須填寫，請勿空白"}),400
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:          
            if user_email:      
                mycursor.execute("SELECT id FROM user WHERE email=%s",[user_email])
                result=mycursor.fetchone()       
                user_id=result["id"]
                # #檢查是否有預定的行程
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
@booking_blueprint.route('/api/booking',methods=['DELETE'])
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

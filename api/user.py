from flask import request
from flask import *
from flask import render_template
from flask import make_response 
from flask import session
from mysql.connector import pooling
from flask import jsonify 
from flask_jwt_extended import  jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
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


user_blueprint = Blueprint('user_blueprint', __name__)

# 會員註冊
@user_blueprint.route('/api/user',methods=['POST'])
def register():
    try:
        #檢查使用者名稱是否存在
        data=request.json
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
@user_blueprint.route('/api/user/auth',methods=['GET'])
@jwt_required()
def auth_get():
    try:
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            email=get_jwt_identity()
            if email:
                mycursor.execute("SELECT id,name,email FROM user WHERE email=%s",[email])
                user=mycursor.fetchone()
                response= jsonify({"data":user})
                return response
            else:
                return jsonify({"error":True,"message":"尚未登入"}),403

    except Exception as e:
            return {"error": True, "message": str(e)},500

    finally:
        connection_object.close()


@user_blueprint.route('/api/user/auth',methods=['PUT','DELETE'])
def auth():
    try:
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            # 會員登入
            if request.method=='PUT':
                data=request.get_json()
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


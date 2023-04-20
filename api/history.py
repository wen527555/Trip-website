from flask import request
from flask import *
from flask import render_template
from flask import make_response 
from flask import session
from mysql.connector import pooling
from flask import jsonify 
from flask_jwt_extended import  jwt_required,get_jwt_identity
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


history_blueprint = Blueprint('history_blueprint', __name__)

#建立購物清單
@history_blueprint.route('/api/history',methods=['GET'])
@jwt_required()
def history_get():
    try:
        user_email=get_jwt_identity()
        if not user_email:
            return jsonify({"error":True,"message":"未登入，拒絕存取"}),403
        connection_object=connection_pooling.get_connection()
        with connection_object.cursor(dictionary=True) as mycursor:
            mycursor.execute("SELECT id FROM user WHERE email=%s",[user_email])
            result=mycursor.fetchone()       
            user_id=result["id"]
            mycursor.execute("SELECT * FROM orders WHERE user_id=%s",[user_id])
            history_data=mycursor.fetchall()
            if history_data:
                return jsonify({"data":history_data})
            else:
                return jsonify({"data":None,"message":"沒有歷史訂單"}) 
            
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}),500

    finally:
        connection_object.close()
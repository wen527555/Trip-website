from os import access
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
        mycursor=connection_object.cursor(dictionary=True)
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
        return {"error": True, "message": str(e)}

    finally:
        mycursor.close()
        connection_object.close()   

@app.route("/api/attraction/<attractionId>", methods=['GET'])
def get_attraction(attractionId):
    try:
        connection_object=connection_pooling.get_connection()
        mycursor=connection_object.cursor(dictionary=True)

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
        mycursor.close()
        connection_object.close()

@app.route("/api/categories", methods=['GET'])
def get_categories():
    try:
        connection_object=connection_pooling.get_connection()
        mycursor=connection_object.cursor(dictionary=True)
        mycursor.execute("SELECT DISTINCT category FROM attractions")
        results=mycursor.fetchall()
        categories=[result['category'] for result in results ]
        return {"data":categories}
    except Exception as e:
        return {"error": True, "message": str(e)}

    finally:
        mycursor.close()
        connection_object.close()



# 會員註冊
@app.route('/api/user',methods=['POST'])
def register():
    try:
        #檢查使用者名稱是否存在
        data=request.get_json()
        print(data)
        name=data["name"]
        password=data["password"]
        email=data["email"]
        connection_object=connection_pooling.get_connection()
        mycursor=connection_object.cursor(dictionary=True)
        mycursor.execute("SELECT email FROM user WHERE email=%s",[email,])
        user=mycursor.fetchone()
        if user is None:
            hashed_password = generate_password_hash(password, method='sha256')
            mycursor.execute("INSERT INTO user (name,email,password) VALUES( %s, %s, %s)",[name,email,hashed_password])
            connection_object.commit()  
            print("註冊成功")          
            return jsonify({"ok":True}),200

        #使用者名稱不存在，新增使用者
        elif not name or not password or not email:
            return{"error":True,"message":"所有欄位皆須填寫，請勿空白"}
        else:
            response={
                "error":True,
                "message":"此email已註冊過，請登入"
            }
            print("註冊失敗，此email已註冊過")   
            return jsonify(response),400
            

    except Exception as e:
        return {"error": True, "message": str(e)}

    finally:
        mycursor.close()
        connection_object.close()


@app.route('/api/user/auth',methods=['GET'])
@jwt_required()
def auth_get():
    try:
        connection_object=connection_pooling.get_connection()
        mycursor=connection_object.cursor(dictionary=True)
        email=get_jwt_identity()
        mycursor.execute("SELECT id,name,email FROM user WHERE email=%s",[email])
        user=mycursor.fetchone()
        response= jsonify({"data":user}) 
        return response
        

    except Exception as e:
            return {"error": True, "message": str(e)},500


    finally:
        mycursor.close()
        connection_object.close()

@app.route('/api/user/auth',methods=['PUT','DELETE'])

def auth():
    try:
        connection_object=connection_pooling.get_connection()
        mycursor=connection_object.cursor(dictionary=True) 

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
                print(response)
                response.set_cookie("access_token", access_token,  secure=False, domain='172.20.10.12',path='/')
                return response


        # 會員登出
        elif request.method=='DELETE':
            response=make_response({"ok":True})
            response.delete_cookie("access_token")
            return response

    except Exception as e:
        return {"error": True, "message": str(e)}

    finally:
        mycursor.close()
        connection_object.close()




app.run(host='0.0.0.0',port=3000,debug=True)




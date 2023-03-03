from flask import Flask
from flask import request
from flask import *
from flask import render_template
from flask import make_response 
from flask import session
from mysql.connector import pooling
from flask import jsonify 
import math


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
        #設定回傳格式
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
        #關閉SQL資料庫連接
        mycursor.close()
        connection_object.close()   

@app.route("/api/attraction/<attractionId>", methods=['GET'])
def get_attraction(attractionId):
    try:
        connection_object=connection_pooling.get_connection()
        mycursor=connection_object.cursor(dictionary=True)
        #取得指定ID的景點資料
        mycursor.execute("SELECT * FROM attractions WHERE id=%s ",(attractionId,))
        results=mycursor.fetchone()
        #找不到對應的景點
        if not results:
            return{"error":True,"message":"景點編號不正確"}
        #將景點資料轉換成需要的格式
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
        #關閉SQL資料庫連接
        mycursor.close()
        connection_object.close()

@app.route("/api/categories", methods=['GET'])
def get_categories():
    try:
        #連結SQL資料庫
        connection_object=connection_pooling.get_connection()
        mycursor=connection_object.cursor(dictionary=True)
        mycursor.execute("SELECT DISTINCT category FROM attractions")
        results=mycursor.fetchall()
        categories=[result['category'] for result in results ]
        #回傳JSON格式資料給客戶端
        return {"data":categories}
    except Exception as e:
        # 將錯誤訊息轉換為字符串，然後返回
        return {"error": True, "message": str(e)}

    finally:
        #關閉SQL資料庫連接
        mycursor.close()
        connection_object.close()

app.run(host='0.0.0.0',port=3000,debug=True)
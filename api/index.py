from flask import request
from flask import *
from flask import render_template
from flask import make_response 
from flask import session
from mysql.connector import pooling
from flask import jsonify 
import math
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

index_blueprint = Blueprint('index_blueprint', __name__)

@index_blueprint.route("/api/attractions", methods=['GET'])
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


@index_blueprint.route("/api/attraction/<attractionId>", methods=['GET'])
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

#景點分類
@index_blueprint.route("/api/categories", methods=['GET'])
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
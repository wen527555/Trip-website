import json
from mysql.connector import pooling
import json,re
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

#讀取JSON檔

with open("data/taipei-attractions.json","r",encoding="utf-8") as file:
    data=json.load(file)

#取得景點清單
lis=data["result"]["results"]

#上傳景點資料到資料庫
for view in lis:
    name=view["name"]
    # print(f'{name}')
    lng=view["longitude"]
    # print(f'{lng}')
    lat=view["latitude"]
    transport=view["direction"]
    mrt=view["MRT"]
    cat=view["CAT"]
    description=view["description"]
    address=view["address"]
    image1=view["file"].split("https")
    # print(f'{image1}')
    image2 = ["https"+x for x in image1 if re.search("JPG", x)]
    image3 = ["https"+x for x in image1 if re.search("jpg", x)]
    images=",".join(image2+image3)

#將景點資料上傳資料庫
sql="INSERT INTO attractions (name, lng, lat,transport, mrt, cat, description,address,images) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
val=(name, lng, lat,transport, mrt, cat, description,address,images)

try:
    #要求連接資料庫
    with connection_pooling.get_connection() as connection_object:
        mycursor=connection_object.cursor()
        mycursor.exectue(sql,val)
        connection_object.commit()
        print("f'{name} upload successful!")
except Exception as e:
    print("f'{name} upload failed!Error:{e}")

finally:
    mycursor.close()
    connection_object.close()



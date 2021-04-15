from sqlalchemy import create_engine
import pymysql
import pandas as pd

engine = create_engine("mariadb+mariadbconnector://testUser@127.0.0.1:3306/test")
conn = engine.connect()

test = {
        "18": {
        "link": "ok",
        "level": [
            "A2", "A2.1", "A2.2",
            "B1", "B1.1", "B1.2",
            "-keine-"
        ],
        "grammar": [
            "Genitiv",
            "Dativ",
            "-keine-"
        ],
        "keywords": [
            "-keine-"
        ]
    },
    "19": {
        "link": "http://www.duden.de",
        "level": [
            "B2", "B2.1", "B2.2",
            "C1", "C1.1", "C1.2",
            "-keine-"
        ],
        "grammar": [
            "Akkusativ",
            "-keine-"
        ],
        "keywords": [
            "-keine-"
        ]
    }
}

def push_to_sql(json_dict, conn):
    trans = conn.begin()
    for v in json_dict.values():
        url = v["link"]
        for el in v["grammar"]:
            print(el)
            conn.execute(
                f"""
                SELECT grammarid
                FROM grammarkeywords
                WHERE grammarval = "{el}"
                INTO @gramid;
                """)
            conn.execute(
                f"""
                SELECT urlid
                FROM url
                WHERE urlval = "{url}"
                INTO @urlid;
                """)
            conn.execute(
                f"""
                INSERT IGNORE INTO url_grammar (urlid, grammarid)
                VALUES (@urlid, @gramid);
                """)
    trans.commit()
    conn.close()

push_to_sql(test, conn)

#trans = conn.begin()
#test_data = conn.execute("SELECT * FROM url_grammar").fetchall()
#conn.close()

#for row in test_data:
 #   print(row)

#cars = {'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
 #       'Price': [["1", "2"],["sds"],["asd","", "sds"],["aso", "sld"]]
  #      }

#df = pd.DataFrame(cars, columns= ['Brand', 'Price'])
#df_temp = df.copy()
#df_temp['Price'] = df_temp['Price'].apply(','.join)
#table_name = "cars"

#df_temp.to_sql(table_name, db_connection, if_exists='replace')

#frame           = pd.read_sql("select * from test.cars", db_connection)
#frame['Price'] = frame['Price'].apply(lambda x: x.split(",y"))
#print(frame)
#db_connection.close()
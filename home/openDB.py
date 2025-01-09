import mysql.connector
def open():
    conn = mysql.connector.connect(
        host="",
        user="",
        password="",
        database="radius"
    )
    # conn = mysql.connector.connect(
    #     host="",
    #     user="",
    #     password="",
    #     database="radius"
    # )
    #print(1)
    return conn
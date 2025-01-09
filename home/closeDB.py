import mysql.connector
def close(conn):
    conn.close()
    # print("close DB")
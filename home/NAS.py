import mysql.connector
from . import openDB
from . import closeDB
def get_data():
    # Kết nối đến cơ sở dữ liệu MySQL
    conn=openDB.open()
    cursor = conn.cursor()
        # Viết truy vấn SQL
    sql_query = "SELECT id,nasname,shortname,description FROM nas"
        # Thực thi truy vấn
    cursor.execute(sql_query)
        # Lấy tất cả các dòng kết quả
    rows = cursor.fetchall()
        #rows =rows.decode('utf-8')
        # In ra tất cả các dòng kết quả
    
    decoded_rows = []

    for row in rows:
        #print((row[2]))
        decoded_row = [item.decode('utf-8') if isinstance(item, (bytes, bytearray)) else item for item in row]
        decoded_rows.append(decoded_row)
        # Đóng cursor và kết nối
    cursor.close()
    closeDB.close(conn)
    return decoded_rows
    
def search_nas(querry):
    conn=openDB.open()
    cursor = conn.cursor()
    querry = querry.upper()
    sql_query= f"""
        SELECT id,nasname,shortname, description 
        FROM nas
        WHERE UPPER(id) LIKE '%{querry}%' 
            OR UPPER(nasname) LIKE '%{querry}%' 
            OR UPPER(shortname) LIKE '%{querry}%'
            OR UPPER(description) LIKE '%{querry}%'
    """
    cursor.execute(sql_query)
        # Lấy tất cả các dòng kết quả
    rows = cursor.fetchall()
        #rows =rows.decode('utf-8')
        # In ra tất cả các dòng kết quả
    
    decoded_rows = []
    for row in rows:
        #print((row[2]))
        decoded_row = [item.decode('utf-8') if isinstance(item, (bytes, bytearray)) else item for item in row]
        decoded_rows.append(decoded_row)
        # Đóng cursor và kết nối
    cursor.close()
    closeDB.close(conn)
    return decoded_rows
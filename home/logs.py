from . import openDB
from . import closeDB

def get_log():
    conn = openDB.open()
    cursor = conn.cursor()
    # Viết truy vấn SQL
    sql_query = "SELECT id, username, iproute, reply,MAC, authdate FROM radpostauth"
    # Thực thi truy vấn
    cursor.execute(sql_query)
    # Lấy tất cả các dòng kết quả
    rows = cursor.fetchall()
    # Đảo ngược thứ tự các dòng kết quả
    rows_reversed = rows[::-1]
    # Chuyển đổi dòng kết quả sang kiểu utf-8 nếu cần
    decoded_rows = []
    for row in rows_reversed:
        decoded_row = [item.decode('utf-8') if isinstance(item, (bytes, bytearray)) else item for item in row]
        decoded_rows.append(decoded_row)
    # Đóng cursor và kết nối
    cursor.close()
    closeDB.close(conn)
    return decoded_rows

def search_logs(querry):
    conn = openDB.open()
    cursor = conn.cursor()
    querry1=querry
    if ':' in querry:
        querry1 = querry.replace(':', '-')

                
    # Viết truy vấn SQL
    sql_query = f"""
        SELECT id, username, iproute, reply, MAC, authdate 
        FROM radpostauth 
        WHERE username LIKE '%{querry}%' 
            OR iproute LIKE '%{querry}%' 
            OR reply LIKE '%{querry}%'
            OR MAC LIKE '%{querry}%'
            OR authdate LIKE '%{querry}%'
            OR MAC LIKE '%{querry1}%'
    """
    # Thực thi truy vấn
    cursor.execute(sql_query)
    # Lấy tất cả các dòng kết quả
    rows = cursor.fetchall()
    # Đảo ngược thứ tự các dòng kết quả
    rows_reversed = rows[::-1]
    # Chuyển đổi dòng kết quả sang kiểu utf-8 nếu cần
    decoded_rows = []
    for row in rows_reversed:
        decoded_row = [item.decode('utf-8') if isinstance(item, (bytes, bytearray)) else item for item in row]
        decoded_rows.append(decoded_row)
    # Đóng cursor và kết nối    
    cursor.close()
    closeDB.close(conn)
    return decoded_rows

def get_log(page_number, rows_per_page):
    conn = openDB.open()
    cursor = conn.cursor()
    print(page_number, rows_per_page)
    # Tính chỉ số bắt đầu và kết thúc của dòng kết quả cần lấy
    start_index = (page_number - 1) * rows_per_page

    # Viết truy vấn SQL với phân trang và sử dụng phương thức parameterized
    sql_query = "SELECT id, username, iproute, reply, MAC, authdate FROM radpostauth ORDER BY id DESC LIMIT %s, %s"

    # Thực thi truy vấn với các tham số được truyền vào
    cursor.execute(sql_query, (start_index, rows_per_page))

    # Lấy tất cả các dòng kết quả
    rows = cursor.fetchall()

    # Chuyển đổi dòng kết quả sang kiểu utf-8 nếu cần
    decoded_rows = []
    for row in rows:
        decoded_row = [item.decode('utf-8') if isinstance(item, (bytes, bytearray)) else item for item in row]
        decoded_rows.append(decoded_row)

    # Đóng cursor và kết nối
    cursor.close()
    closeDB.close(conn)

    return decoded_rows

def get_max_val(query):
    conn = openDB.open()
    cursor = conn.cursor()
    query1=query
    if ':' in query:
        query1 = query.replace(':', '-')   
    
    if query =='' :
        sql_query_count=f"""
                        SELECT MAX(id) 
                        FROM radpostauth
                    """
    else:
        sql_query_count = f"""
            SELECT COUNT(*) as total
            FROM radpostauth 
            WHERE username LIKE '%{query}%' 
                OR iproute LIKE '%{query}%' 
                OR reply LIKE '%{query}%' 
                OR MAC LIKE '%{query}%' 
                OR authdate LIKE '%{query}%' 
                OR MAC LIKE '%{query1}%'
"""
    # Truy vấn để lấy id lớn nhất (id cuối cùng)
    cursor.execute(sql_query_count)
    max_id = cursor.fetchone()[0]

    cursor.close()
    closeDB.close(conn)

    return max_id

val=""
def get_data_AC():
    import mysql.connector
    from . import openDB
    from . import closeDB
    # Kết nối đến cơ sở dữ liệu MySQL
    conn=openDB.open()
    cursor = conn.cursor()
        # Viết truy vấn SQL
    sql_query = """
        SELECT
            username,
            COUNT(*) AS count
        FROM
            radpostauth
        WHERE
            authdate >= CURDATE()
            AND reply = 'Access-Accept'  -- Sửa điều kiện ở đây
        GROUP BY
            username
        ORDER BY
            count DESC
        LIMIT 10;
    """

        # Thực thi truy vấn
    cursor.execute(sql_query)
        # Lấy tất cả các dòng kết quả
    rows = cursor.fetchall()
        #rows =rows.decode('utf-8')
        # In ra tất cả các dòng kết quả
    
    decoded_rows = []
    if not rows:
        for _ in range(5):
            decoded_rows.append([val] * 2)  # number_of_columns là số lượng cột trong mỗi hàng
    else:
        for row in rows:
            #print((row[2]))
            decoded_row = [item.decode('utf-8') if isinstance(item, (bytes, bytearray)) else item for item in row]
            decoded_rows.append(decoded_row)
            # Đóng cursor và kết nối
        while len(decoded_rows) < 5:
            decoded_rows.append([val] * len(decoded_rows[0]))
    cursor.close()
    closeDB.close(conn)  
    return decoded_rows


def get_data_Rj():
    from . import openDB
    from . import closeDB
    # import openDB
    # import closeDB
    # Kết nối đến cơ sở dữ liệu MySQL
    conn=openDB.open()
    cursor = conn.cursor()
        # Viết truy vấn SQL
    sql_query = """
        SELECT
            username,
            COUNT(*) AS count
        FROM
            radpostauth
        WHERE
            authdate >= CURDATE()
            AND reply = 'Access-Reject'  -- Sửa điều kiện ở đây
        GROUP BY
            username
        ORDER BY
            count DESC
        LIMIT 10;
    """
    cursor.execute(sql_query)
        # Lấy tất cả các dòng kết quả
    rows = cursor.fetchall()
        #rows =rows.decode('utf-8')
        # In ra tất cả các dòng kết quả
    
    decoded_rows = []
    if not rows:
        for _ in range(5):
            decoded_rows.append([val] * 2)  # number_of_columns là số lượng cột trong mỗi hàng
    else:
        for row in rows:
            #print((row[2]))
            decoded_row = [item.decode('utf-8') if isinstance(item, (bytes, bytearray)) else item for item in row]
            decoded_rows.append(decoded_row)
            # Đóng cursor và kết nối
        while len(decoded_rows) < 5:
            decoded_rows.append([val] * len(decoded_rows[0]))
    cursor.close()
    closeDB.close(conn)
    return decoded_rows
# print(get_data_Rj())
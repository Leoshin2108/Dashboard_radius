import matplotlib.pyplot as plt
import io
import base64
from . import openDB
from . import closeDB


def get_chart_home():
    conn = openDB.open()
    cursor = conn.cursor()

    # Truy vấn SQL để lấy tổng số lần Access-Accept và Access-Reject trong một ngày
    sql = """
        SELECT 
            SUM(CASE WHEN reply = 'Access-Accept' THEN 1 ELSE 0 END) AS total_access_accept_count,
            SUM(CASE WHEN reply = 'Access-Reject' THEN 1 ELSE 0 END) AS total_access_reject_count
        FROM radpostauth
        WHERE DATE(authdate) = CURDATE()
    """
    cursor.execute(sql)
    result = cursor.fetchone()
    data=[]
    #print(result)
    if result[0] != None:
        data.append(int(result[0]))
    else:
         data.append(0)
    if result[1] != None:
        data.append(int(result[1]))
    else:
         data.append(0)
    # Đóng kết nối
    cursor.close()
    closeDB.close(conn)
    return data

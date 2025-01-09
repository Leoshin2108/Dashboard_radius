# views.py
import matplotlib.pyplot as plt
import io
import base64
import mysql.connector
from datetime import datetime
from . import openDB
from . import closeDB
# import openDB
# import closeDB
def month():
    conn1 = mysql.connector.connect(
        host="172.20.240.1",
        user="radius",
        password="Vnpt@lan",
        database="radius"
    )
    current_month = 3#datetime.now().month
    # Tạo kết nối đến cơ sở dữ liệu
    cursor = conn1.cursor()
    sql = f"""
        SELECT 
            COUNT(CONVERT_TZ(AcctStartTime, 'UTC', '+7:00')), 
            DAY(CONVERT_TZ(AcctStartTime, 'UTC', '+7:00')) AS Day 
        FROM 
            radacct 
        WHERE 
            MONTH(CONVERT_TZ(AcctStartTime, 'UTC', '+7:00')) = {current_month} 
        GROUP BY 
            DAY(CONVERT_TZ(AcctStartTime, 'UTC', '+7:00'))
    """

    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn1.close()
        # Tạo list chứa dữ liệu cho biểu đồ
    days = []
    counts = []
    for row in rows:
        days.append(row[1])
        counts.append(row[0])
    #print()
        # Vẽ biểu đồ
    plt.figure(figsize=(12, 6))
    bars=plt.bar(days, counts)
    plt.xlabel('Day')
    plt.ylabel('Count')
    plt.title('Alltime Login records based on Daily distribution')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom',rotation=0)
        # Lưu biểu đồ vào buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
        # Encode biểu đồ thành base64 string
    graph = base64.b64encode(image_png).decode('utf-8')

    # Trả về hình ảnh biểu đồ dưới dạng HTTP response
    return graph

def daily():
    # Kết nối đến cơ sở dữ liệu
    conn=openDB.open()
    specific_day = datetime.now().day
    current_month = datetime.now().month
    
    cursor = conn.cursor()
    sql = f"""
        SELECT 
            HOUR(AcctStartTime) AS Hour, 
            COUNT(*) AS Count 
        FROM 
            radacct 
        WHERE 
            DAY(AcctStartTime) = {specific_day} 
            AND MONTH(AcctStartTime) = {current_month} 
        GROUP BY 
            HOUR(AcctStartTime)
    """

    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    # print(conn)
    # Tạo list chứa dữ liệu cho biểu đồ
    # Tạo danh sách cho 24 giờ và gán giá trị 0 cho mỗi giờ
    counts = [0] * 24
    for row in rows:
        counts[row[0]]=row[1]
    return counts
   
# daily()
def yearly():
    conn1 = mysql.connector.connect(
        host="172.20.240.1",
        user="radius",
        password="Vnpt@lan",
        database="radius"
    )
    specific_year =2024 #datetime.now().month
    # Tạo kết nối đến cơ sở dữ liệu
    cursor = conn1.cursor()
    sql = f"""
        SELECT 
            YEAR(CONVERT_TZ(AcctStartTime, 'UTC', '+7:00')) AS Year, 
            COUNT(*) AS Count 
        FROM 
            radacct 
        GROUP BY 
            YEAR(CONVERT_TZ(AcctStartTime, 'UTC', '+7:00'))
    """



    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn1.close()
        # Tạo list chứa dữ liệu cho biểu đồ
    days = []
    counts = []
    for row in rows:
        #print(row)
        days.append(row[0])
        counts.append(row[1])
    
        # Vẽ biểu đồ
    plt.figure(figsize=(12, 6))
    bars=plt.bar(days, counts)
    plt.xlabel('Day')
    plt.ylabel('Count')
    plt.title('Alltime Login records based on Daily distribution')
    plt.xticks(days)  # Chỉ hiển thị các số nguyên trên trục x
    plt.grid(True)
    plt.tight_layout()
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom',rotation=0)
        # Lưu biểu đồ vào buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
        # Encode biểu đồ thành base64 string
    graph = base64.b64encode(image_png).decode('utf-8')

    # Trả về hình ảnh biểu đồ dưới dạng HTTP response
    return graph
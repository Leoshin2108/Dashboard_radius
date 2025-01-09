# views.py
from django.http import HttpResponse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator
import datetime
import pytz
from .import openDB
from .import closeDB
import datetime
# import openDBz``
# import closeDB
desired_timezone = pytz.timezone('Asia/Bangkok')  # Múi giờ +7 (Giờ Đông Á)

# Lấy thời gian hiện tại dựa trên múi giờ bạn đã thiết lập
current_datetime = datetime.datetime.now(desired_timezone)

# In thời gian hiện tại
# print(current_datetime)

def generate_minute_data_chart():
    conn = openDB.open()
    cursor = conn.cursor()
    current_datetime = datetime.datetime.now(desired_timezone).replace(second=0, microsecond=0)
    # print(current_datetime)
    # print("Mở cơ sở dữ liệu")
    data = []
    # Truy vấn SQL để lấy dữ liệu cho mỗi điểm thời gian
    for i in range(15):  # Lấy dữ liệu cho mỗi phút trong 10 phút   
        start_time = current_datetime - datetime.timedelta(minutes=i) + datetime.timedelta(minutes=1)
        end_time = start_time - datetime.timedelta(minutes=1)  
        # print(start_time,end_time)
        sql = f"""
            SELECT 
                DATE_FORMAT(authdate, '%H:%i') AS time_interval, 
                SUM(CASE WHEN reply = 'Access-Accept' THEN 1 ELSE 0 END) AS accept_count,
                SUM(CASE WHEN reply = 'Access-Reject' THEN 1 ELSE 0 END) AS reject_count
            FROM radpostauth
            WHERE authdate BETWEEN '{end_time}' AND '{start_time}'
            GROUP BY time_interval
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        t=[]
        t=end_time.strftime('%H:%M')
        #print(t)
        if results:
            # Chuyển đổi kết quả thành kiểu dữ liệu int
            converted_results = []
            for result in results:
                time_interval =result[0]
                accept_count = int(result[1])
                reject_count = int(result[2])
                converted_results.append((time_interval, accept_count, reject_count))
            data.extend(converted_results)
        else:
            # Nếu không có kết quả, thêm dữ liệu với giá trị mặc định 0
            # print(1)
            data.append((end_time.strftime('%H:%M'), 0, 0))
        # print(data)
        # print()
    # print("Đóng cơ sở dữ liệu")
    cursor.close()
    closeDB.close(conn)
    
    return data
generate_minute_data_chart()
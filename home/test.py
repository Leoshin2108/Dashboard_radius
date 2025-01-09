import mysql.connector
import matplotlib.pyplot as plt
import io
import base64

def daily():
    # Kết nối đến cơ sở dữ liệu
    conn = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
    
    specific_day = 10  # Thay đổi thành ngày cụ thể bạn muốn vẽ biểu đồ
    current_month = 3  # Thay đổi thành datetime.now().month nếu muốn sử dụng tháng hiện tại
    
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
    
    hours = list(range(24))
    counts = [0] * 24
    for row in rows:
        counts[row[0]]=row[1]
    # Tạo list chứa dữ liệu cho biểu đồ
    # hours = [row[0] for row in rows]
    # counts = [row[1] for row in rows]

    # Vẽ biểu đồ cột
    plt.figure(figsize=(12, 6))
    bars = plt.bar(hours, counts)
    plt.xlabel('Hour')
    plt.ylabel('Count')
    plt.title(f'Alltime Login records for day {specific_day} in month {current_month}')
    plt.xticks(hours)  # Đảm bảo tất cả các giờ được hiển thị trên trục x
    plt.grid(True)
    plt.tight_layout()

    # Hiển thị số liệu trên từng cột
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', rotation=0)

    # Lưu biểu đồ vào buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode biểu đồ thành base64 string
    graph = base64.b64encode(image_png).decode('utf-8')

    # Trả về hình ảnh biểu đồ dưới dạng chuỗi base64
    return graph

# Vẽ biểu đồ và lưu kết quả vào một biến
graph = daily()

# In biểu đồ
plt.show()

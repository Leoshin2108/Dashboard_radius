from . import openDB
from . import closeDB
from datetime import timedelta
def search(start,end):
        
    # print(start,end)
    temp=(end-start)
    # print(temp)
    
    if temp <= timedelta(days=3):
        ac,rj,hour=hours(start,end)
        
    elif temp >timedelta(days=3) and temp <timedelta(days=45) :
        ac,rj,hour=day(start,end)
    else:
         ac,rj,hour=monthly(start,end)
        
    # print(ac)
    # print(rj)
    # print(hour)   
    return ac,rj, hour

def hours(start, end):
    conn = openDB.open()
    cursor = conn.cursor()
    sql = f"""
        SELECT 
            DATE_FORMAT(authdate, '%Y-%m-%d %H:00:00') AS DateHour, 
            SUM(CASE WHEN reply = 'Access-Accept' THEN 1 ELSE 0 END) AS AcceptCount,
            SUM(CASE WHEN reply = 'Access-Reject' THEN 1 ELSE 0 END) AS RejectCount
        FROM 
            radpostauth 
        WHERE 
            authdate >= '{start}' 
            AND authdate <= '{end}' 
        GROUP BY 
            DATE_FORMAT(authdate, '%Y-%m-%d %H:00:00')
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    accept_list = [int(result[1]) for result in results]
    reject_list = [int(result[2]) for result in results]
    datetime_list = [result[0] for result in results]
    conn.close()
    return accept_list,reject_list, datetime_list

def day(start,end):
    conn = openDB.open()
    cursor = conn.cursor()
    sql = f"""
        SELECT 
            DATE(authdate) AS Date,
            SUM(CASE WHEN reply = 'Access-Accept' THEN 1 ELSE 0 END) AS AcceptCount,
            SUM(CASE WHEN reply = 'Access-Reject' THEN 1 ELSE 0 END) AS RejectCount
        FROM 
            radpostauth 
        WHERE 
            authdate >= '{start}' 
            AND authdate <= '{end}' 
        GROUP BY 
            DATE(authdate)

    """
    cursor.execute(sql)
    results = cursor.fetchall()
    accept_list = [int(result[1]) for result in results]
    reject_list = [int(result[2]) for result in results]
    datetime_list = [result[0] for result in results]
    date_str_list = [date_obj.strftime("%Y-%m-%d") for date_obj in datetime_list]
    conn.close()
    return accept_list,reject_list, date_str_list

def monthly(start,end):
    conn = openDB.open()
    cursor = conn.cursor()
    sql = f"""
        SELECT 
            DATE_FORMAT(authdate, '%Y-%m') AS Month,
            SUM(CASE WHEN reply = 'Access-Accept' THEN 1 ELSE 0 END) AS AcceptCount,
            SUM(CASE WHEN reply = 'Access-Reject' THEN 1 ELSE 0 END) AS RejectCount
        FROM 
            radpostauth 
        WHERE 
            authdate >= '{start}' 
            AND authdate <= '{end}' 
        GROUP BY 
            DATE_FORMAT(authdate, '%Y-%m')
    """
    cursor.execute(sql)
    results = cursor.fetchall()

    accept_list = [int(result[1]) for result in results]
    reject_list = [int(result[2]) for result in results]
    month_list = [result[0] for result in results]

    conn.close()

    return accept_list, reject_list, month_list

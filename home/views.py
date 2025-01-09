from django.shortcuts import render, redirect
from . import NAS
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponseRedirect
from . import graplifetime
from . import over_login_home
# import datetime
import pytz
from . import charts_search
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from . import get_top_ac_rj
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from . import logs
from . import filter_str

desired_timezone = pytz.timezone('Asia/Bangkok')  # Múi giờ +7 (Giờ Đông Á)
# Thiết lập múi giờ mặc định cho Python
datetime.now(desired_timezone)
# Create your views here.
# @login_required
def nas(request):
        search_value = request.session.get('search_value_nas', '')
        selected_value = request.session.get('session_max_rows', '25')
        if request.method == 'POST':
            if 'session_max_rows' in request.POST:    
                selected_value = request.POST.get('session_max_rows')
                request.session['session_max_rows'] = selected_value
            if 'search_value_nas' in request.POST:
                # search_value =request.POST.get('search_value','')
                search_value =filter_str.clean_sql(request.POST.get('search_value_nas', '')) 
                # Lưu giá trị tìm kiếm vào session
                print(search_value)
                request.session['search_value_nas'] = search_value
                
        if search_value!="":
            data=NAS.search_nas(search_value)
        else:
            data=NAS.get_data()
        # print(selected_value)
        
        paginator = Paginator(data, selected_value)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'home/nas.html',{'page_obj': page_obj,'session_max_rows': selected_value,'data_search':search_value})
# @login_required
def chart(request):
    if request.method == 'POST':
        start_time_str=request.POST.get('time_start')
        end_time_str=request.POST.get('time_end')
        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
        # print(start_time,end_time)
        ac,rj,hours=charts_search.search(start_time,end_time)
    else:
        start_time = datetime.now(desired_timezone).replace(hour=0, minute=0, second=0)
        end_time = datetime.now(desired_timezone).replace(hour=23, minute=59, second=59)
        ac,rj,hours=charts_search.search(start_time,end_time)    
    chart_data = {
        'ac': ac,
        'rj': rj,
        'hours': hours
    }
    chart_data=json.dumps(chart_data)
    # print(chart_data)
    # print(start_time.replace(tzinfo=None),end_time.replace(tzinfo=None))
    return render(request,'home/chart.html',{'chart_data':chart_data,'start_time':start_time,'end_time':end_time})      

def home(request):
    rj=get_top_ac_rj.get_data_Rj()
    ac=get_top_ac_rj.get_data_AC()
    return render(request, "home/home.html",{'rj':rj,'ac':ac})

def get_chart_home(request):
    data=graplifetime.generate_minute_data_chart()
    times = [item[0] for item in data]
    accept_counts = [item[1] for item in data]
    reject_counts = [item[2] for item in data]
    #print(data)
    return JsonResponse(data={
        'labels': times,
        'accept': accept_counts,
        'reject' :reject_counts
    })
    
def get_over_AC_RJ(request):
    data=over_login_home.get_chart_home()
    return JsonResponse(data={
        'ac':data[0],
        'rj': data[1]
    })

def login_radius(request):
     return render(request, "home/login.html")

def my_view(request):
    # Lấy tên người dùng và mật khẩu từ request (ví dụ: từ form submission)
    username = request.POST.get('username')
    password = request.POST.get('password')
    # Xác thực bằng RADIUS
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        # Đăng nhập người dùng
        login(request, user)
        return redirect('home') #render(request, "home/home.html")#HttpResponse("Xác thực thành công!")
    else:
        return HttpResponse("Xác thực thất bại.")

def get_logs(request):
    search_value = request.GET.get('search', '')
    take_val = request.session.get('session_max_rows', 25)
    # print(
    count_val=(logs.get_max_val(search_value))
    total_page =int(count_val / int(take_val))+1 #xuwr ly lam` tron so `
    page_number = request.GET.get('page',1) 
    # print(page_number)
    next_page=int(page_number) +1
    pre_page=int(page_number) -1
    # print(next_page,pre_page)
    if next_page > int(count_val):
        next_page=count_val
    if pre_page < 1:
        pre_page=1
    # print(next_page,pre_page)
    if request.method == 'POST':
        if 'session_max_rows' in request.POST:    
            take_val = request.POST.get('session_max_rows')
            request.session['session_max_rows'] = take_val
            total_page =int(count_val / int(take_val))+1
        if 'search_value' in request.POST:
            search_value =filter_str.clean_sql(request.POST.get('search_value', '')) 
            # Lưu giá trị tìm kiếm vào session
            # request.session['search_value'] = search_value

    if search_value != '': 
            data=logs.search_logs(search_value)
            paginator = Paginator(data, take_val)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request,'home/logs.html',{'page_obj': page_obj,'data_search':search_value,
            'session_max_rows': take_val,'total_page':total_page,'page_number':page_number,'pre_page':pre_page,'next_page':next_page})
        
    else:

        # skip_val=int((int(page_number)-1)*int(take_val))
        data=logs.get_log(int(page_number),int(take_val))
        #print(search_value)                
        paginator = Paginator(data, take_val)
        print(request.GET.get('search'))
        page_obj = paginator.get_page(page_number)
        return render(request,'home/logs.html',{'page_obj': page_obj,'data_search':search_value,
        'session_max_rows': take_val,'total_page':total_page,'page_number':page_number,'pre_page':pre_page,'next_page':next_page})



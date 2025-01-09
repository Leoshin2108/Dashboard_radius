"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home,name='home'),
    path('login_auth/',views.my_view,name='login_auth'),
    path('nas/',views.nas),
    path('login/',views.login_radius),
    path('chart/',views.chart),
    path('logs/',views.get_logs),
    path('get_chart_home/',views.get_chart_home,name='get_chart_home'),
    path('chart_AC_RJ/',views.get_over_AC_RJ,name='chart_AC_RJ'),
    # path('chart_get_AC_daily/',views.chart_get_AC_daily,name='chart_get_AC_daily')
]


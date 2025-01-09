FROM python:3.8

# Cài đặt các dependencies của hệ thống
RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập môi trường Python
ENV PYTHONUNBUFFERED 1
RUN python3 -m pip install --upgrade pip

# Tạo thư mục chứa mã nguồn của Django
RUN mkdir /app
WORKDIR /app

# Copy requirements.txt và cài đặt dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn Django vào thư mục làm việc
COPY . /app/

# Chạy các lệnh migrate và collectstatic
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Mở cổng 8000 để phục vụ ứng dụng Django
EXPOSE 8000

# Khởi chạy ứng dụng Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

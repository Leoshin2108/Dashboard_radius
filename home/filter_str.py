import html
def clean_html(input_data):
    # Sử dụng html.escape() để escape các ký tự HTML đặc biệt
    clean_data = html.escape(input_data)

    return clean_data
def clean_sql(input_data):
    # Loại bỏ các ký tự đặc biệt có thể được sử dụng trong SQL Injection
    clean_data = input_data.replace("'", "").replace('"', '')

    return clean_data
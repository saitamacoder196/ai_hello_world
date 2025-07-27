# AI Hello World Django REST Framework API

## Mô tả
Đây là một project Django REST Framework hiển thị API "AI Hello World!".

## Cấu trúc Project
```
ai_hello_world/
├── manage.py
├── ai_hello_world/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── hello/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    └── serializers.py
```

## Cách chạy project

1. Đảm bảo Django và DRF đã được cài đặt:
   ```
   pip install django djangorestframework
   ```

2. Chạy migration:
   ```
   cd d:\02_Workshop\ai_hello_world
   python manage.py migrate
   ```

3. Khởi chạy server:
   ```
   python manage.py runserver
   ```

## API Endpoints

### 1. Function-based API View
- **URL**: http://127.0.0.1:8000/
- **URL**: http://127.0.0.1:8000/api/hello/
- **Method**: GET
- **Response**:
```json
{
    "message": "AI Hello World!",
    "welcome": "Chào mừng bạn đến với Django REST Framework API!",
    "timestamp": "2025-07-25T10:30:00.123456Z",
    "status": "success"
}
```

### 2. Class-based API View
- **URL**: http://127.0.0.1:8000/api/hello-world/
- **Method**: GET
- **Response**:
```json
{
    "data": {
        "message": "AI Hello World!",
        "welcome": "Chào mừng bạn đến với Django REST Framework API!",
        "timestamp": "2025-07-25T10:30:00.123456Z",
        "status": "success"
    },
    "api_version": "1.0",
    "endpoint": "/api/hello-world/",
    "method": "GET"
}
```

### 3. Browsable API
- **URL**: http://127.0.0.1:8000/api-auth/
- Giao diện web để test API trực tiếp

## Cách test API

### Sử dụng curl:
```bash
curl -X GET http://127.0.0.1:8000/api/hello/
curl -X GET http://127.0.0.1:8000/api/hello-world/
```

### Sử dụng trình duyệt:
Truy cập các URL trên trình duyệt để xem JSON response

## Tính năng đã thêm:
- ✅ Django REST Framework
- ✅ Serializer để chuẩn hóa dữ liệu
- ✅ Function-based API View với decorator @api_view
- ✅ Class-based API View kế thừa APIView
- ✅ JSON Response với timestamp
- ✅ HTTP status codes
- ✅ Browsable API interface
- ✅ Multiple endpoints

# AI Hello World API Server

Resource Management System APIs với mock data cho frontend development.

## 🚀 Quick Start

### 1. Cài đặt Dependencies

```bash
# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Cài đặt packages
pip install -r requirements.txt
```

### 2. Chạy Server

```bash
# Cách 1: Sử dụng script
python run_server.py

# Cách 2: Chạy trực tiếp
DJANGO_SETTINGS_MODULE=development_settings python manage.py runserver 0.0.0.0:8000
```

### 3. Truy cập API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 📋 Available APIs

### System APIs
- `GET /api/v1/status` - API system status

### Authentication APIs (Mock)
- `POST /api/v1/auth/simple/login` - Simple login (always success)

### Resource Management APIs
- `GET /api/v1/idle-resources/simple` - Get idle resources list
- `GET /api/v1/idle-resources/simple/{id}` - Get resource detail

### Master Data APIs
- `GET /api/v1/master-data/simple` - Get master data (departments, job ranks, etc.)

## 🔧 API Testing

### Using curl

```bash
# Test login
curl -X POST http://localhost:8000/api/v1/auth/simple/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user", "password": "any_password"}'

# Test resource list
curl -X GET "http://localhost:8000/api/v1/idle-resources/simple?page=1&page_size=10"

# Test master data
curl -X GET "http://localhost:8000/api/v1/master-data/simple"
```

### Using Python

```python
import requests

# Login
response = requests.post('http://localhost:8000/api/v1/auth/simple/login', 
                        json={'username': 'test_user', 'password': 'test'})
print(response.json())

# Get resources
response = requests.get('http://localhost:8000/api/v1/idle-resources/simple')
print(response.json())
```

## 📄 API Response Examples

### Login Response
```json
{
  "success": true,
  "message": "Login successful",
  "user_id": "uuid",
  "username": "test_user",
  "access_token": "mock_token_12345",
  "expires_in": 3600
}
```

### Resource List Response
```json
{
  "records": [
    {
      "id": "uuid",
      "employee_name": "Nguyễn Văn A",
      "employee_id": "EMP001",
      "department_name": "Development",
      "job_rank": "Senior",
      "idle_type": "Bench",
      "idle_from_date": "2025-01-01",
      "idle_to_date": "2025-12-31"
    }
  ],
  "total_count": 100,
  "page_info": {
    "current_page": 1,
    "total_pages": 5,
    "has_next_page": true
  }
}
```

## 🔒 Security Note

⚠️ **Development Only**: Các APIs này sử dụng mock data và không có authentication thực tế. Chỉ dùng cho development và testing.

## 📞 Support

- Development Team: dev@company.com
- Swagger Documentation: http://localhost:8000/api/docs/

## 🎯 Next Steps

1. **Frontend Integration**: Sử dụng Swagger UI để hiểu API structure
2. **Mock Data**: Tất cả responses đều là mock data cố định
3. **Real Implementation**: Sau khi frontend hoàn thành, sẽ implement logic thực tế
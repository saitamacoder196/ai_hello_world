# 🔧 CORS Fix Guide

## ❌ Problem
Khi truy cập Swagger UI tại `http://localhost:8000/api/docs/`, gặp lỗi:
```
Failed to fetch.
Possible Reasons:
- CORS
- Network Failure  
- URL scheme must be "http" or "https" for CORS request
```

## ✅ Solution

### 1. CORS đã được cấu hình

File `development_settings.py` đã bao gồm:

```python
# CORS settings
INSTALLED_APPS += ['corsheaders']

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be first
    # ... other middleware
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
```

### 2. Start Server với đúng settings

```bash
# Đảm bảo dùng development_settings
cd "/mnt/d/00. Workshop/ai_hello_world"
source venv/bin/activate
DJANGO_SETTINGS_MODULE=development_settings python manage.py runserver 0.0.0.0:8000
```

### 3. Hoặc sử dụng script có sẵn

```bash
python run_server.py
```

## 🧪 Verify CORS hoạt động

Chạy test để kiểm tra:

```bash
python test_cors_django.py
```

Expected output:
```
✅ CORS is properly configured
✅ Swagger UI should work without CORS errors
✅ Frontend can make API calls
```

## 🌐 Access Points

Sau khi start server:

- **Server**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔍 Troubleshooting

### Nếu vẫn gặp CORS error:

1. **Check server đang chạy**:
   ```bash
   curl http://localhost:8000/api/v1/status
   ```

2. **Check CORS headers**:
   ```bash
   curl -H "Origin: http://localhost:3000" -v http://localhost:8000/api/v1/status
   ```

3. **Restart server** với development settings:
   ```bash
   pkill -f "python.*runserver"
   DJANGO_SETTINGS_MODULE=development_settings python manage.py runserver 0.0.0.0:8000
   ```

### Browser Cache Issues:

1. **Hard refresh** Swagger UI page (Ctrl+F5)
2. **Clear browser cache** cho localhost:8000
3. **Disable browser cache** trong DevTools

## ✅ Verification

Sau khi fix, bạn sẽ thấy:

1. **Swagger UI loads** không có lỗi CORS
2. **APIs appear** trong Swagger documentation  
3. **Test requests work** từ Swagger UI
4. **Response data** hiển thị đúng mock data

## 🎯 Next Steps

1. ✅ Swagger UI accessible
2. ✅ APIs documented with examples
3. ✅ Mock data ready for frontend
4. ✅ CORS enabled for development

Frontend team có thể:
- View API documentation tại Swagger UI
- Test APIs directly từ browser
- Integrate với mock endpoints
- Develop UI components với real API structure
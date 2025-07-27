# CORS Configuration for Django API

## Problem
When testing APIs from a browser or frontend application, you may encounter CORS (Cross-Origin Resource Sharing) errors like:
- `Failed to fetch`
- `URL scheme must be "http" or "https" for CORS request`
- `Access to fetch at 'http://127.0.0.1:8000/api/...' from origin 'null' has been blocked by CORS policy`

## Solution
This project has been configured with `django-cors-headers` to handle CORS issues during development.

## Configuration Details

### 1. Installed Package
```bash
pip install django-cors-headers==4.3.1
```

### 2. Settings Configuration
In `ai_hello_world/settings.py`:

**Added to INSTALLED_APPS:**
```python
'corsheaders',  # Add CORS headers support
```

**Added to MIDDLEWARE (at the top):**
```python
'corsheaders.middleware.CorsMiddleware',  # Add CORS middleware first
```

**CORS Settings:**
```python
# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080", 
    "http://127.0.0.1:8080",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

# For development, allow all origins (NOT for production)
CORS_ALLOW_ALL_ORIGINS = True

# Allow credentials to be included in CORS requests
CORS_ALLOW_CREDENTIALS = True

# Additional CORS headers
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding', 
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Update ALLOWED_HOSTS for development
ALLOWED_HOSTS = ['*']  # For development only
```

## How to Run

### Option 1: Manual
```bash
# Install dependency
pip install django-cors-headers==4.3.1

# Run server
python manage.py runserver 0.0.0.0:8000
```

### Option 2: Use Scripts
**Linux/Mac:**
```bash
chmod +x run_with_cors.sh
./run_with_cors.sh
```

**Windows:**
```batch
run_with_cors.bat
```

## Testing CORS

### 1. Using the Test HTML File
Open `cors_test.html` in your browser and click "Test API Call" button.

### 2. Using cURL
```bash
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://127.0.0.1:8000/api/v1/idle-resources/
```

### 3. Using JavaScript Fetch
```javascript
fetch('http://127.0.0.1:8000/api/v1/idle-resources/', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

## Production Considerations

⚠️ **Important:** The current configuration allows all origins (`CORS_ALLOW_ALL_ORIGINS = True`) which is suitable for development only.

For production, you should:

1. Set `CORS_ALLOW_ALL_ORIGINS = False`
2. Specify exact origins in `CORS_ALLOWED_ORIGINS`
3. Set proper `ALLOWED_HOSTS`
4. Enable HTTPS

Example production settings:
```python
# Production CORS settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

## Common Issues and Solutions

### Issue 1: "Failed to fetch"
**Solution:** Make sure the Django server is running and accessible at the URL you're trying to fetch.

### Issue 2: "CORS policy" error
**Solution:** Verify that `corsheaders.middleware.CorsMiddleware` is at the top of your MIDDLEWARE list.

### Issue 3: Credentials not being sent
**Solution:** Set `CORS_ALLOW_CREDENTIALS = True` and include credentials in your fetch request:
```javascript
fetch(url, {
    credentials: 'include',
    // ... other options
})
```

### Issue 4: Custom headers not allowed
**Solution:** Add your custom headers to `CORS_ALLOW_HEADERS` list.

## API Endpoints Available
All endpoints now support CORS:
- `GET /api/v1/idle-resources/` - List idle resources
- `POST /api/v1/idle-resources/` - Create idle resource  
- `GET /api/v1/idle-resources/{id}/` - Get idle resource detail
- `PUT /api/v1/idle-resources/{id}/` - Update idle resource
- `DELETE /api/v1/idle-resources/{id}/` - Delete idle resource
- And all other endpoints listed in `API_ENDPOINTS_LIST.md`

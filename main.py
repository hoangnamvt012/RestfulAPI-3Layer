# File: main.py

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
# Cần import logic lỗi từ file exceptions.py
from exceptions import APIException, ERROR_MAPPING 
# Import router đã được quản lý version
from api_router import api_router 

# Khởi tạo ứng dụng
app = FastAPI(title="Company API") 

# GLOBAL EXCEPTION HANDLER
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    # SỬA LỖI: Lấy HTTP Status Code chuẩn từ bảng ánh xạ, dùng exc.error_code
    http_status_code = ERROR_MAPPING.get(exc.error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JSONResponse(
        status_code=http_status_code,
        content={
            "code": exc.error_code,   # SỬA TỪ exc.code -> exc.error_code
            "message": exc.detail     # SỬA TỪ exc.message -> exc.detail
        },
    )

# APPLICATION ROUTERS: Gắn router đã được quản lý version
app.include_router(api_router)
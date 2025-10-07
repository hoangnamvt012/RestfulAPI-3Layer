# File: main.py (Đã sửa)

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
# Cần import logic lỗi từ file exceptions.py
from exceptions import APIException, ERROR_MAPPING 
# Import router đã được quản lý version
from api_router import api_router 

# Khởi tạo ứng dụng
app = FastAPI(title="Company API") 

# GLOBAL EXCEPTION HANDLER (Giả định logic này của bạn)
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    # Sử dụng ERROR_MAPPING để trả về status code và chi tiết lỗi chuẩn
    error_detail = ERROR_MAPPING.get(exc.code, {"status_code": 500, "message": "Internal Server Error"})
    
    return JSONResponse(
        status_code=error_detail["status_code"],
        content={
            "code": exc.code,
            "message": exc.message 
        },
    )

# APPLICATION ROUTERS: Gắn router đã được quản lý version
# main.py giờ đây không cần biết về /v1 hay /v2
app.include_router(api_router) 

# LƯU Ý: Nếu bạn có Dependency Injection (get_uow), chúng vẫn được giữ nguyên.
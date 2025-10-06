# File: main.py

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from exceptions import APIException, ERROR_MAPPING
# Cập nhật import Controllers từ thư mục presentation:
from presentation import employee_controller, department_controller 
# Cập nhật import UoW từ thư mục dal:
from dal.unit_of_work import UnitOfWork, get_uow 

app = FastAPI(title="COMPANY API")

# GLOBAL EXCEPTION HANDLER: Bắt APIException và ánh xạ sang HTTP Status
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    """Bắt APIException từ Service, tra cứu mã HTTP Status và trả về lỗi."""
    
    http_status_code = ERROR_MAPPING.get(exc.error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JSONResponse(
        status_code=http_status_code,
        content={"detail": exc.detail, "error_code": exc.error_code}, 
    )

# APPLICATION ROUTERS
app.include_router(employee_controller.router, prefix="/employees", tags=["employees"])
app.include_router(department_controller.router, prefix="/departments", tags=["departments"])
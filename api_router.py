# File: api_router.py (File mới)

from fastapi import APIRouter
from presentation.department_controller import router as department_router
from presentation.employee_controller import router as employee_router

# Khởi tạo một Router gốc để chứa tất cả các Version
api_router = APIRouter()

# --- KHAI BÁO VERSION 1 (/v1) ---
# Gắn các controller vào tiền tố /v1 để quản lý version

api_router.include_router(
    department_router,
    prefix="/v1/departments",  # Versioning được thêm vào đây
    tags=["Department", "v1"]
)

api_router.include_router(
    employee_router,
    prefix="/v1/employees",  # Versioning được thêm vào đây
    tags=["Employee", "v1"]
)

# Ví dụ nếu có Version 2, bạn sẽ thêm tiếp dòng dưới đây:
# api_router.include_router(employee_v2_router, prefix="/v2/employees", tags=["Employee", "v2"])
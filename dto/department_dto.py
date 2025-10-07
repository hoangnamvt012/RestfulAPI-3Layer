# File: dto/department_dto.py (ĐÃ SỬA TRIỆT ĐỂ)

from typing import List, Generic, TypeVar, Optional
from datetime import datetime
from pydantic import BaseModel, Field
# Giữ lại GenericModel import nhưng sửa lại để tương thích Pydantic V2
# HOẶC có thể đổi thành: from pydantic import BaseModel, Field, Generic, TypeVar 
# nhưng tạm thời giữ GenericModel để tránh thay đổi quá lớn.

T = TypeVar('T') 

# --- DTO CHUNG: PHÂN TRANG (Pagination DTO) ---
class PaginationResponseDto(BaseModel, Generic[T]):
    data: List[T] = Field(..., description="Danh sách các đối tượng") 
    skip: int = Field(0, description="Số lượng bản ghi bị bỏ qua")
    limit: int = Field(100, description="Số lượng bản ghi tối đa trong phản hồi này")
    total_count: int = Field(..., description="Tổng số bản ghi trong hệ thống")
    
    class Config:
        # ✅ KHẮC PHỤC CẢNH BÁO: Đổi schema_extra -> json_schema_extra
        json_schema_extra = {
            "example": {
                "data": [
                    {"id": 1, "code": "DEPT-240101-100", "name": "IT Infrastructure", "status": "Active"},
                ],
                "skip": 0,
                "limit": 100,
                "total_count": 2
            }
        }


# --- DTO CHO HÀNH ĐỘNG CREATE & PUT (Khắc phục lỗi Import) ---
class DepartmentCreateUpdateDto(BaseModel): 
    name: str = Field(
        ..., 
        min_length=3,
        max_length=50,
        title="Tên Phòng Ban",
        description="Tên phòng ban. Bắt buộc và không được trùng lặp."
    )
    status: str = Field("Active", description="Trạng thái hoạt động của phòng ban") 


# --- DTO CHO HÀNH ĐỘNG RESPONSE ---
class DepartmentResponseDto(BaseModel):
    id: int
    code: str 
    name: str
    status: str
    created_at: Optional[datetime] = Field(None, description="Thời gian tạo bản ghi") 
    updated_at: Optional[datetime] = Field(None, description="Thời gian cập nhật gần nhất")

    class Config:
        # ✅ KHẮC PHỤC CẢNH BÁO: Đổi orm_mode -> from_attributes
        from_attributes = True 
        # ✅ KHẮC PHỤC CẢNH BÁO: Đổi schema_extra -> json_schema_extra
        json_schema_extra = { 
            "example": {
                "id": 1,
                "code": "DEPT-240101-100",
                "name": "IT Infrastructure",
                "status": "Active",
                "created_at": "2025-01-01T10:00:00",
                "updated_at": "2025-10-07T14:30:00"
            }
        }
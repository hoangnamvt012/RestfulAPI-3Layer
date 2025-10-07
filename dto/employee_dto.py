# File: dto/employee_dto.py (ĐÃ SỬA TRIỆT ĐỂ)

from typing import Optional, List, Generic, TypeVar
from datetime import datetime
from pydantic import BaseModel, Field, conint

T = TypeVar('T') 


# --- DTO CHUNG: PHÂN TRANG (Tái định nghĩa lại để đảm bảo tính độc lập) ---
class PaginationResponseDto(BaseModel, Generic[T]):
    data: List[T] = Field(..., description="Danh sách các đối tượng") 
    skip: int = Field(0, description="Số lượng bản ghi bị bỏ qua")
    limit: int = Field(100, description="Số lượng bản ghi tối đa")
    total_count: int = Field(..., description="Tổng số bản ghi")


# --- DTO CHO HÀNH ĐỘNG CREATE & PUT (TẤT CẢ CÁC TRƯỜNG ĐỀU BẮT BUỘC) ---
class EmployeeCreateUpdateDto(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    position: str = Field(..., max_length=50)
    department_id: conint(ge=1) = Field(
        ..., 
        description="ID phòng ban phải là số nguyên dương"
    )
    phone_number: str = Field(..., max_length=10, min_length=10)
    address: str = Field(..., max_length=255)
    cccd: str = Field(..., max_length=12, min_length=12) 
    status: str = Field("Active", max_length=20) 
    
    class Config:
        # ✅ KHẮC PHỤC CẢNH BÁO: Đổi schema_extra -> json_schema_extra
        json_schema_extra = { 
            "example": {
                "name": "Trần Văn B",
                "position": "Senior Developer",
                "department_id": 1,
                "phone_number": "0987654321",
                "address": "Số 10, Đường ABC, TP.HCM",
                "cccd": "001199001234",
                "status": "Active"
            }
        }


# --- DTO CHO HÀNH ĐỘNG RESPONSE ---
class EmployeeResponseDto(BaseModel):
    id: int
    code: str 
    name: str
    position: str
    department_id: int
    phone_number: str
    address: str
    status: str

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        # ✅ KHẮC PHỤC CẢNH BÁO: Đổi orm_mode -> from_attributes
        from_attributes = True 
        # ✅ KHẮC PHỤC CẢNH BÁO: Đổi schema_extra -> json_schema_extra
        json_schema_extra = { 
            "example": {
                "id": 101,
                "code": "EMP-251007-123",
                "name": "Trần Văn B",
                "position": "Senior Developer",
                "department_id": 1,
                "phone_number": "0987654321",
                "address": "Số 10, Đường ABC, TP.HCM",
                "status": "Active",
                "created_at": "2025-10-07T08:00:00",
                "updated_at": "2025-10-07T08:00:00"
            }
        }
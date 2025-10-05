from pydantic import BaseModel, Field, conint
from typing import Optional

# Base DTO cho shared fields
class EmployeeBaseDto(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    position: str = Field(..., max_length=50)
    department_id: conint(ge=1) = Field(
        ..., 
        description="ID phòng ban phải là số nguyên dương"
    )
    # Cập nhật: Thêm trường mới với validation
    phone_number: str = Field(..., max_length=10, min_length=10)
    address: str = Field(..., max_length=255)
    cccd: str = Field(..., max_length=12, min_length=12) 
    status: str = Field("Active", max_length=20)


class EmployeeCreateDto(EmployeeBaseDto):
    pass

# DTO cho Cập nhật (PATCH/PUT)
class EmployeeUpdateDto(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    position: Optional[str] = Field(None, max_length=50)
    department_id: Optional[conint(ge=1)] = None
    phone_number: Optional[str] = Field(None, max_length=10, min_length=10)
    address: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, max_length=20)
    
    class Config:
        extra = 'forbid' # Không cho phép trường dữ liệu không có trong DTO

class EmployeeResponseDto(EmployeeBaseDto):
    id: int
    code: str 

    class Config:
        orm_mode = True
from pydantic import BaseModel, Field, conint

# DTO Cơ sở dùng chung
class EmployeeBaseDto(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    position: str = Field(..., max_length=50)
    # Validation: Đảm bảo FK là số nguyên dương
    department_id: conint(ge=1) = Field(
        ..., 
        description="ID phòng ban phải là số nguyên dương"
    )

class EmployeeCreateDto(EmployeeBaseDto):
    pass

class EmployeeResponseDto(EmployeeBaseDto):
    id: int
    # Thêm ID Nghiệp vụ vào phản hồi
    code: str 

    class Config:
        orm_mode = True
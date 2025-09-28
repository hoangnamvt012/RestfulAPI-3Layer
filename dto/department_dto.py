from pydantic import BaseModel, Field

class DepartmentCreateDto(BaseModel):
    # Nâng cấp Validation: Thêm ràng buộc độ dài
    name: str = Field(
        ..., 
        min_length=3,
        max_length=50,
        title="Tên Phòng Ban"
    )

class DepartmentResponseDto(BaseModel):
    id: int
    # Thêm ID Nghiệp vụ vào phản hồi
    code: str 
    name: str

    class Config:
        orm_mode = True



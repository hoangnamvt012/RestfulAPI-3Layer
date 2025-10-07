# File: presentation/department_controller.py (Đã sửa)

from fastapi import APIRouter, Depends, Query, status, HTTPException
from dal.unit_of_work import UnitOfWork, get_uow
from bus.department_service import DepartmentService
from dto.department_dto import (
    DepartmentCreateUpdateDto,
    DepartmentResponseDto, 
    PaginationResponseDto
)
from exceptions import APIException

router = APIRouter()

# [R] GET LIST (Paging)
# Đã sửa response_model để trả về OBJECT (PaginationResponseDto)
@router.get("/", response_model=PaginationResponseDto[DepartmentResponseDto])
async def get_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    uow: UnitOfWork = Depends(get_uow)
):
    service = DepartmentService(uow.repo)
    # Giả định service.get_all() trả về (items, total_count)
    items, total_count = service.get_all(skip=skip, limit=limit)
    
    # Trả về Object chuẩn hóa (đã khắc phục lỗi Array)
    return PaginationResponseDto[DepartmentResponseDto](
        data=items,
        skip=skip,
        limit=limit,
        total_count=total_count
    )

# ... (GET BY ID, CREATE, DELETE giữ nguyên)

# [U] UPDATE (Dùng PUT thay cho PATCH)
@router.put("/{department_id}", response_model=DepartmentResponseDto) # SỬA TỪ PATCH -> PUT
async def update_department(department_id: int, dto: DepartmentCreateUpdateDto, uow: UnitOfWork = Depends(get_uow)): # SỬA DTO
    # Với PUT, dùng model_dump() để lấy TẤT CẢ các trường (vì tất cả đều bắt buộc trong DTO)
    update_data = dto.model_dump(by_alias=True) 
    
    try:
        updated_department = DepartmentService(uow.repo).update_department(department_id, update_data)
        uow.commit()
        return updated_department
    except APIException as e:
        uow.rollback()
        raise e
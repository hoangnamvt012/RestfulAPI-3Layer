# File: presentation/employee_controller.py (Đã sửa)
from fastapi import APIRouter, Depends, Query, status, HTTPException
from main import get_uow, UnitOfWork 
# ... (Các imports giữ nguyên)
from dto.employee_dto import (
    EmployeeCreateUpdateDto,
    EmployeeResponseDto, 
    PaginationResponseDto # DTO cho API Get List
)

router = APIRouter()

# [R] GET LIST (Paging)
# Đã sửa response_model để trả về OBJECT (PaginationResponseDto)
@router.get("/", response_model=PaginationResponseDto[EmployeeResponseDto])
async def get_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    uow: UnitOfWork = Depends(get_uow)
):
    service = EmployeeService(uow.repo)
    # Giả định service.get_all() trả về (items, total_count)
    items, total_count = service.get_all(skip=skip, limit=limit)
    
    # Trả về Object chuẩn hóa (đã khắc phục lỗi Array)
    return PaginationResponseDto[EmployeeResponseDto](
        data=items,
        skip=skip,
        limit=limit,
        total_count=total_count
    )

# ... (Các endpoints khác giữ nguyên)

# [U] UPDATE (PUT đã đúng, chỉ cần sửa DTO)
@router.put("/{employee_id}", response_model=EmployeeResponseDto)
async def update_employee(employee_id: int, dto: EmployeeCreateUpdateDto, uow: UnitOfWork = Depends(get_uow)): # SỬA DTO
    update_data = dto.model_dump(by_alias=True) 
    try:
        updated_employee = EmployeeService(uow.repo).update_employee(employee_id, update_data)
        uow.commit() 
        return updated_employee
    except APIException as e:
        uow.rollback() 
        raise e
# File: presentation/employee_controller.py

from fastapi import APIRouter, Depends, Query, status, HTTPException
# SỬA LỖI: Import Dependency Injection từ module gốc (DAL)
from dal.unit_of_work import get_uow, UnitOfWork 
from bus.employee_service import EmployeeService
from dto.employee_dto import (
    EmployeeCreateUpdateDto,
    EmployeeResponseDto, 
    PaginationResponseDto # DTO cho API Get List
)
from exceptions import APIException

router = APIRouter()

# [R] GET LIST (Paging) - Đã sửa response_model để trả về OBJECT (PaginationResponseDto)
@router.get("/", response_model=PaginationResponseDto[EmployeeResponseDto])
async def get_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    uow: UnitOfWork = Depends(get_uow)
):
    service = EmployeeService(uow.repo)
    items, total_count = service.get_all(skip=skip, limit=limit)
    
    # Trả về Object chuẩn hóa (đã khắc phục lỗi Array)
    return PaginationResponseDto[EmployeeResponseDto](
        data=items,
        skip=skip,
        limit=limit,
        total_count=total_count
    )

# [R] GET BY ID
@router.get("/{employee_id}", response_model=EmployeeResponseDto)
async def get_employee_by_id(employee_id: int, uow: UnitOfWork = Depends(get_uow)):
    service = EmployeeService(uow.repo)
    employee = service.get_employee_by_id(employee_id)
    return employee

# [C] CREATE
@router.post("/", response_model=EmployeeResponseDto, status_code=status.HTTP_201_CREATED)
async def create_employee(dto: EmployeeCreateUpdateDto, uow: UnitOfWork = Depends(get_uow)):
    service = EmployeeService(uow.repo)
    new_employee = service.create_employee(dto)
    uow.commit()
    uow.refresh(new_employee)
    return new_employee

# [U] UPDATE (Dùng PUT)
@router.put("/{employee_id}", response_model=EmployeeResponseDto)
async def update_employee(employee_id: int, dto: EmployeeCreateUpdateDto, uow: UnitOfWork = Depends(get_uow)):
    service = EmployeeService(uow.repo)
    updated_employee = service.update_employee(employee_id, dto)
    uow.commit()
    uow.refresh(updated_employee)
    return updated_employee

# [D] DELETE
@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: int, uow: UnitOfWork = Depends(get_uow)):
    service = EmployeeService(uow.repo)
    service.delete_employee(employee_id)
    uow.commit()
    return None
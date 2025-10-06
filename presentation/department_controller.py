# File: presentation/department_controller.py

from fastapi import APIRouter, Depends, Query, status, HTTPException
from dal.unit_of_work import UnitOfWork, get_uow
# Import từ thư mục bus:
from bus.department_service import DepartmentService
# Import từ thư mục dto:
from dto.department_dto import DepartmentCreateDto, DepartmentResponseDto 
from typing import List
from exceptions import APIException

router = APIRouter()

# [R] GET LIST (Paging)
@router.get("/", response_model=List[DepartmentResponseDto])
async def get_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    uow: UnitOfWork = Depends(get_uow)
):
    return DepartmentService(uow.repo).get_all(skip=skip, limit=limit)

# [R] GET BY ID
@router.get("/{department_id}", response_model=DepartmentResponseDto)
async def get_department_by_id(department_id: int, uow: UnitOfWork = Depends(get_uow)):
    return DepartmentService(uow.repo).get_department_by_id(department_id)

# [C] CREATE
@router.post("/", response_model=DepartmentResponseDto, status_code=status.HTTP_201_CREATED)
async def create_department(dto: DepartmentCreateDto, uow: UnitOfWork = Depends(get_uow)):
    try:
        new_department = DepartmentService(uow.repo).create_department(dto)
        uow.commit()
        return new_department
    except APIException as e:
        uow.rollback()
        raise e 

# [U] UPDATE (Dùng PATCH)
@router.patch("/{department_id}", response_model=DepartmentResponseDto)
async def update_department(department_id: int, dto: DepartmentCreateDto, uow: UnitOfWork = Depends(get_uow)):
    update_data = dto.dict(exclude_unset=True) 
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update.")
    
    try:
        updated_department = DepartmentService(uow.repo).update_department(department_id, update_data)
        uow.commit()
        return updated_department
    except APIException as e:
        uow.rollback()
        raise e

# [D] DELETE
@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(department_id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        DepartmentService(uow.repo).delete_department(department_id)
        uow.commit()
        return None
    except APIException as e:
        uow.rollback()
        raise e
# File: presentation/employee_controller.py

from fastapi import APIRouter, Depends, Query, status, HTTPException
from dal.unit_of_work import UnitOfWork, get_uow
# Import từ thư mục bus:
from bus.employee_service import EmployeeService 
# Import từ thư mục dto:
from dto.employee_dto import EmployeeCreateDto, EmployeeResponseDto 
from typing import List
from exceptions import APIException

router = APIRouter()

# [R] GET LIST (Paging)
@router.get("/", response_model=List[EmployeeResponseDto])
async def get_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    uow: UnitOfWork = Depends(get_uow)
):
    return EmployeeService(uow.repo).get_all(skip=skip, limit=limit)

# [R] GET BY ID
@router.get("/{employee_id}", response_model=EmployeeResponseDto)
async def get_employee_by_id(employee_id: int, uow: UnitOfWork = Depends(get_uow)):
    return EmployeeService(uow.repo).get_employee_by_id(employee_id)

# [C] CREATE
@router.post("/", response_model=EmployeeResponseDto, status_code=status.HTTP_201_CREATED)
async def create_employee(dto: EmployeeCreateDto, uow: UnitOfWork = Depends(get_uow)):
    try:
        new_employee = EmployeeService(uow.repo).create_employee(dto)
        uow.commit() # COMMIT nếu thành công
        return new_employee
    except APIException as e:
        uow.rollback() # ROLLBACK nếu lỗi nghiệp vụ
        raise e 

# [U] UPDATE (Dùng PUT)
@router.put("/{employee_id}", response_model=EmployeeResponseDto)
async def update_employee(employee_id: int, dto: EmployeeCreateDto, uow: UnitOfWork = Depends(get_uow)):
    update_data = dto.dict() 
    try:
        updated_employee = EmployeeService(uow.repo).update_employee(employee_id, update_data)
        uow.commit() # COMMIT nếu thành công
        return updated_employee
    except APIException as e:
        uow.rollback() # ROLLBACK nếu lỗi nghiệp vụ
        raise e 

# [D] DELETE
@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        EmployeeService(uow.repo).delete_employee(employee_id)
        uow.commit() # COMMIT nếu thành công
        return None 
    except APIException as e:
        uow.rollback() # ROLLBACK nếu lỗi nghiệp vụ
        raise e
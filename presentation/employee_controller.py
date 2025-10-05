from fastapi import APIRouter, Depends, status
from dal.unit_of_work import UnitOfWork, get_uow # 👈 Import UoW và DI
from bus.employee_service import EmployeeService
from dto.employee_dto import EmployeeCreateDto, EmployeeResponseDto, EmployeeUpdateDto
from typing import List

# Hàm DI mới sử dụng UoW
def get_employee_service(uow: UnitOfWork = Depends(get_uow)) -> EmployeeService:
    # 👈 Truyền RepositoryGroup từ UoW vào Service
    return EmployeeService(uow.repo)

router = APIRouter(prefix="/employees", tags=["Employees"])

# POST: CREATE
@router.post("/", response_model=EmployeeResponseDto, status_code=status.HTTP_201_CREATED)
def create_employee(dto: EmployeeCreateDto, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        # Service chỉ tạo đối tượng
        new_employee = EmployeeService(uow.repo).create_employee(dto)
        uow.commit() # Commit toàn bộ giao dịch
        uow.refresh(new_employee) # Làm mới đối tượng để lấy ID
        return new_employee

# GET: LIST và GET by ID giữ nguyên (không cần commit)
# ...

# PATCH: PARTIAL UPDATE
@router.patch("/{employee_id}", response_model=EmployeeResponseDto)
def update_employee(employee_id: int, dto: EmployeeUpdateDto, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        # Service sẽ chỉ cập nhật các trường có trong DTO
        updated_employee = EmployeeService(uow.repo).update_employee(employee_id, dto)
        uow.commit()
        uow.refresh(updated_employee)
        return updated_employee

# DELETE: DELETE
@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        result = EmployeeService(uow.repo).delete_employee(employee_id)
        uow.commit() # Commit giao dịch xóa
        return result
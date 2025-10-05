from fastapi import APIRouter, Depends, status
from dal.unit_of_work import UnitOfWork, get_uow # 👈 Import UoW và DI
from bus.department_service import DepartmentService
from dto.department_dto import DepartmentCreateDto, DepartmentResponseDto
from typing import List, Optional

# Hàm DI mới sử dụng UoW
def get_department_service(uow: UnitOfWork = Depends(get_uow)) -> DepartmentService:
    # 👈 Truyền RepositoryGroup từ UoW vào Service
    return DepartmentService(uow.repo) 

router = APIRouter(prefix="/departments", tags=["Departments"])

# POST: CREATE
@router.post("/", response_model=DepartmentResponseDto, status_code=status.HTTP_201_CREATED)
def create_department(dto: DepartmentCreateDto, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        # Service chỉ tạo đối tượng
        new_department = DepartmentService(uow.repo).create_department(dto)
        uow.commit() # Commit toàn bộ giao dịch
        uow.refresh(new_department) # Làm mới đối tượng để lấy ID
        return new_department

# GET: LIST và GET by ID giữ nguyên (không cần commit)
# ...

# PUT: UPDATE
@router.put("/{department_id}", response_model=DepartmentResponseDto)
def update_department(department_id: int, dto: DepartmentCreateDto, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        updated_department = DepartmentService(uow.repo).update_department(department_id, dto)
        uow.commit()
        uow.refresh(updated_department)
        return updated_department

# DELETE: DELETE
@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, uow: UnitOfWork = Depends(get_uow)):
    with uow:
        result = DepartmentService(uow.repo).delete_department(department_id)
        uow.commit() # Commit giao dịch xóa
        return result   
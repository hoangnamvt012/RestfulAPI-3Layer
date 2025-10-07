# File: bus/department_service.py

from typing import Dict, Any, List
from dal.unit_of_work import RepositoryGroup # Import từ dal
from datetime import datetime
from exceptions import APIException
from random import randint 
# Giả định import DTOs từ thư mục dto:
from dto.department_dto import DepartmentCreateUpdateDto, DepartmentResponseDto

class DepartmentService:
    def __init__(self, uow: RepositoryGroup):
        self.repo = uow 
        
    def _generate_department_code(self):
        date_part = datetime.now().strftime('%y%m%d')
        random_part = randint(100, 999) 
        return f"DEPT-{date_part}-{random_part}"

    # [R] GET BY ID
    def get_department_by_id(self, department_id: int):
        # Truy cập Department Repository qua RepositoryGroup
        department = self.repo.department_repository.get_by_id(department_id) 
        if not department:
            raise APIException(4001, f"Department ID {department_id} not found.") 
        return department

    # [R] GET ALL (Hỗ trợ Paging)
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repo.department_repository.get_all(skip=skip, limit=limit)

    # [C] CREATE
    def create_department(self, dto: DepartmentCreateUpdateDto):
        if self.repo.department_repository.get_by_name(dto.name):
            raise APIException(4091, f"Tên phòng ban '{dto.name}' đã tồn tại.") 
        
        data_for_repo: Dict[str, Any] = dto.dict()
        data_for_repo['code'] = self._generate_department_code() 
        
        return self.repo.department_repository.create(**data_for_repo) 

    # [U] UPDATE (Linh hoạt cho PATCH)
    def update_department(self, department_id: int, dto: DepartmentCreateUpdateDto):
        department = self.get_department_by_id(department_id)
        
        new_name = update_data.get('name')
        
        if (new_name and 
            self.repo.department_repository.get_by_name(new_name) and 
            new_name != department.name):
            
            raise APIException(4091, f"Tên phòng ban '{new_name}' đã tồn tại.")

        return self.repo.department_repository.update(department, update_data)
        
    # [D] DELETE
    def delete_department(self, department_id: int):
        department = self.get_department_by_id(department_id)

        # Truy cập Employee Repository qua RepositoryGroup để kiểm tra khóa ngoại
        if self.repo.employee_repository.count_by_department(department_id) > 0:
            raise APIException(4012, "Không thể xóa phòng ban này vì vẫn còn nhân viên thuộc về nó.")
        
        self.repo.department_repository.delete(department)
        return {"message": f"Department ID {department_id} deleted."}
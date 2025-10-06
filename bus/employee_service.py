# File: bus/employee_service.py

from typing import Dict, Any, List
from dal.unit_of_work import RepositoryGroup # Import từ dal
from datetime import datetime
from exceptions import APIException
from random import randint
# Giả định import DTOs từ thư mục dto:
from dto.employee_dto import EmployeeCreateDto 

class EmployeeService:
    def __init__(self, uow: RepositoryGroup):
        self.repo = uow
    
    def _generate_employee_code(self):
        date_part = datetime.now().strftime('%y%m%d')
        random_part = randint(100, 999) 
        return f"EMP-{date_part}-{random_part}"

    # [R] GET BY ID
    def get_employee_by_id(self, employee_id: int):
        employee = self.repo.employee_repository.get_by_id(employee_id)
        if not employee:
            raise APIException(4001, f"Employee ID {employee_id} not found.") 
        return employee

    # [R] GET ALL (Hỗ trợ Paging)
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repo.employee_repository.get_all(skip=skip, limit=limit)

    # [C] CREATE
    def create_employee(self, dto: EmployeeCreateDto):
        # Kiểm tra Khóa Ngoại: Truy cập Department Repository
        if not self.repo.department_repository.get_by_id(dto.department_id):
            raise APIException(4011, f"Department ID {dto.department_id} không tồn tại.")
        
        if self.repo.employee_repository.get_by_cccd(dto.cccd):
            raise APIException(4091, f"CCCD '{dto.cccd}' đã tồn tại trong hệ thống.")

        data_for_repo: Dict[str, Any] = dto.dict()
        data_for_repo['code'] = self._generate_employee_code() 
        
        return self.repo.employee_repository.create(**data_for_repo)

    # [U] UPDATE (Tuân thủ PUT)
    def update_employee(self, employee_id: int, update_data: Dict[str, Any]):
        employee = self.get_employee_by_id(employee_id)
        
        # Validation Rule: Kiểm tra Khóa Ngoại
        new_dept_id = update_data.get('department_id')
        if new_dept_id and not self.repo.department_repository.get_by_id(new_dept_id):
            raise APIException(4011, f"Department ID {new_dept_id} không tồn tại.")

        # Validation Rule: Kiểm tra CCCD trùng
        new_cccd = update_data.get('cccd')
        if (new_cccd and 
            self.repo.employee_repository.get_by_cccd(new_cccd) and
            new_cccd != employee.cccd):
            raise APIException(4091, f"CCCD '{new_cccd}' đã tồn tại trong hệ thống.")

        return self.repo.employee_repository.update(employee, update_data)
        
    # [D] DELETE
    def delete_employee(self, employee_id: int):
        employee = self.get_employee_by_id(employee_id)
        self.repo.employee_repository.delete(employee)
        return {"message": f"Employee ID {employee_id} deleted."}
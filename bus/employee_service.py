# File: bus/employee_service.py

from typing import Dict, Any, List
from dal.unit_of_work import RepositoryGroup # Import từ dal
from datetime import datetime
from exceptions import APIException
from random import randint
# SỬA LỖI: Import đúng tên DTO
from dto.employee_dto import EmployeeCreateUpdateDto

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
        items = self.repo.employee_repository.get_all(skip=skip, limit=limit)
        total_count = self.repo.employee_repository.get_count()
        return items, total_count

    # [C] CREATE
    def create_employee(self, dto: EmployeeCreateUpdateDto):
        # Kiểm tra Khóa Ngoại
        if not self.repo.department_repository.get_by_id(dto.department_id):
            raise APIException(4011, f"Department ID {dto.department_id} không tồn tại.")
        
        # Kiểm tra CCCD trùng lặp
        if self.repo.employee_repository.get_by_cccd(dto.cccd):
            raise APIException(4091, f"CCCD '{dto.cccd}' đã tồn tại trong hệ thống.")

        # Dùng model_dump() cho create vì tất cả các trường đều bắt buộc
        data_for_repo: Dict[str, Any] = dto.model_dump() 
        data_for_repo['code'] = self._generate_employee_code() 
        
        return self.repo.employee_repository.create(**data_for_repo)

    # [U] UPDATE (Tuân thủ PUT)
    # SỬA LỖI: Thay vì nhận dict, nhận DTO để tận dụng Pydantic Validation
    def update_employee(self, employee_id: int, dto: EmployeeCreateUpdateDto): 
        employee = self.get_employee_by_id(employee_id)
        
        # SỬA LỖI: Lấy dữ liệu từ DTO, chỉ lấy những trường được set (put thường là full update, nhưng dùng exclude_unset=True cho linh hoạt)
        update_data: Dict[str, Any] = dto.model_dump(exclude_unset=True) 

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
from fastapi import HTTPException, status
from dal.unit_of_work import RepositoryGroup 
from datetime import datetime

class EmployeeService:
    def __init__(self, uow: RepositoryGroup):
        # Service giờ chỉ nhận RepositoryGroup (từ UoW)
        self.repo = uow
    
    # ... (_generate_employee_code giữ nguyên)

    def create_employee(self, dto):
        # 1. Validation Rule: Kiểm tra Khóa Ngoại (Department có tồn tại không)
        if not self.repo.departments.get_by_id(dto.department_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Department ID {dto.department_id} không tồn tại."
            )
        
        # 2. Validation Rule: Kiểm tra CCCD duy nhất
        if self.repo.employees.get_by_cccd(dto.cccd):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"CCCD '{dto.cccd}' đã tồn tại trong hệ thống."
            )

        employee_code = self._generate_employee_code() 

        # Truyền cả DTO vào Repository
        return self.repo.employees.create(employee_code, dto)

    def update_employee(self, employee_id: int, dto):
        employee = self.get_employee_by_id(employee_id) # Kiểm tra 404
        
        # 1. Validation Rule: Kiểm tra Khóa Ngoại (Nếu department_id được cập nhật)
        if dto.department_id and not self.repo.departments.get_by_id(dto.department_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Department ID {dto.department_id} không tồn tại."
            )

        update_data = dto.dict(exclude_unset=True) # Chỉ lấy các trường được truyền
        
        # Cập nhật (Repo không commit)
        return self.repo.employees.update(employee, update_data)
        
    def delete_employee(self, employee_id: int):
        employee = self.get_employee_by_id(employee_id) # Kiểm tra 404
        self.repo.employees.delete(employee)
        # Giao dịch sẽ được commit/rollback bởi UoW
        return {"message": f"Employee ID {employee_id} deleted."}

    # ... (get_employee_by_id và list_employees giữ nguyên)
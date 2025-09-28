from fastapi import HTTPException, status
from dal.employee_repository import EmployeeRepository
from dal.department_repository import DepartmentRepository 
from dto.employee_dto import EmployeeCreateDto
from datetime import datetime

class EmployeeService:
    """Xử lý Logic Nghiệp vụ (400, 404) và TẠO ID Nghiệp vụ"""
    def __init__(self, emp_repo: EmployeeRepository, dept_repo: DepartmentRepository):
        self.emp_repo = emp_repo
        self.dept_repo = dept_repo

    def _generate_employee_code(self) -> str:
        """ID Nghiệp vụ: EMP-YYYY-NNNN (Đặt trong Service)"""
        current_year = datetime.now().year
        current_count = self.emp_repo.get_count()
        new_id_number = current_count + 1
        return f"EMP-{current_year}-{new_id_number:04d}" 

    def create_employee(self, dto: EmployeeCreateDto):
        # Logic Nghiệp vụ: Xử lý 400 Bad Request (FK không tồn tại)
        if not self.dept_repo.get_by_id(dto.department_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Department ID {dto.department_id} không tồn tại. Vui lòng tạo phòng ban trước."
            )

        employee_code = self._generate_employee_code() 

        return self.emp_repo.create(employee_code, dto.name, dto.position, dto.department_id)
    
    def list_employees(self):
        return self.emp_repo.get_all()
    
    def get_employee_by_id(self, employee_id: int):
        # Logic Nghiệp vụ: Xử lý 404 Not Found
        employee = self.emp_repo.get_by_id(employee_id)
        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy nhân viên với ID: {employee_id}"
            )
        return employee
from sqlalchemy.orm import Session
from dto.employee_entity import Employee
from typing import List, Optional

class EmployeeRepository:
    """Chỉ xử lý Persistence Logic (Truy vấn DB)"""
    def __init__(self, db: Session):
        self.db = db

    def get_count(self) -> int:
        """Hàm hỗ trợ Service: Đếm tổng số bản ghi (cho tạo code)."""
        return self.db.query(Employee).count()

    def get_all(self) -> List[Employee]:
        return self.db.query(Employee).all()

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

    def create(self, code: str, name: str, position: str, department_id: int) -> Employee:
        """Nhận code Nghiệp vụ từ Service."""
        employee = Employee(
            code=code, 
            name=name, 
            position=position, 
            department_id=department_id
        )
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee
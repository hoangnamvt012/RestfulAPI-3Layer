from sqlalchemy.orm import Session
from dto.department_entity import Department
from typing import List, Optional

class DepartmentRepository:
    """Chỉ xử lý Persistence Logic (Truy vấn DB)"""
    def __init__(self, db: Session):
        self.db = db

    def get_count(self) -> int:
        """Hàm hỗ trợ Service: Đếm tổng số bản ghi (cho tạo code)."""
        return self.db.query(Department).count()

    def get_all(self) -> List[Department]:
        return self.db.query(Department).all()

    def get_by_id(self, department_id: int) -> Optional[Department]:
        return self.db.query(Department).filter(Department.id == department_id).first()
    
    def get_by_name(self, name: str) -> Optional[Department]:
        return self.db.query(Department).filter(Department.name == name).first()
    
    def create(self, code: str, name: str) -> Department:
        """Nhận code Nghiệp vụ từ Service."""
        department = Department(code=code, name=name)
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)
        return department
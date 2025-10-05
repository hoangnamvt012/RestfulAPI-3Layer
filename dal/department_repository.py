from sqlalchemy.orm import Session
from typing import Optional
from dal.base_repository import BaseRepository
from dto.department_entity import Department # Model Entity

# Dùng Dict cho hàm update linh hoạt hơn
from typing import Dict, Any 

class DepartmentRepository(BaseRepository[Department]):
    """Repository chuyên biệt cho Department, kế thừa logic CRUD chung."""
    
    def __init__(self, db: Session):
        # Truyền Session và Model Entity vào BaseRepository
        super().__init__(db, Department) 
    
    # ----------------------------------------------------
    # CHỈ CÁC HÀM ĐẶC THÙ (Specialized Methods)
    # ----------------------------------------------------

    def get_by_name(self, name: str) -> Optional[Department]:
        return self.db.query(self.model).filter(self.model.name == name).first()

    def create(self, **kwargs) -> Department:
        """Sử dụng **kwargs để tạo Entity linh hoạt hơn."""
        department = Department(**kwargs)
        self.db.add(department)
        return department
    
    # Cải thiện: Hàm update linh hoạt
    def update(self, department: Department, update_data: Dict[str, Any]) -> Department:
        """Cập nhật các trường được chỉ định trong update_data."""
        for field, value in update_data.items():
            setattr(department, field, value)
        return department

    # LƯU Ý: Các hàm get_by_id, get_all, delete đã được BaseRepository xử lý
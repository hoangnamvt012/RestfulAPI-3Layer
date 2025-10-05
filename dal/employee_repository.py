from sqlalchemy.orm import Session
from typing import Optional
from dal.base_repository import BaseRepository
from dto.employee_entity import Employee # Model Entity
from typing import Dict, Any 

class EmployeeRepository(BaseRepository[Employee]):
    """Repository chuyên biệt cho Employee, kế thừa logic CRUD chung."""

    def __init__(self, db: Session):
        # Truyền Session và Model Entity vào BaseRepository
        super().__init__(db, Employee)

    # ----------------------------------------------------
    # CHỈ CÁC HÀM ĐẶC THÙ (Specialized Methods)
    # ----------------------------------------------------
    
    def get_by_cccd(self, cccd: str) -> Optional[Employee]:
        """Tìm bản ghi theo CCCD (Validation)"""
        return self.db.query(self.model).filter(self.model.cccd == cccd).first()

    def count_by_department(self, department_id: int) -> int:
        """Đếm nhân viên trong phòng ban (Validation khi xóa Department)"""
        return self.db.query(self.model).filter(self.model.department_id == department_id).count()

    def create(self, **kwargs) -> Employee:
        """Sử dụng **kwargs để tạo Entity linh hoạt hơn."""
        employee = Employee(**kwargs)
        self.db.add(employee)
        return employee

    # Hàm update linh hoạt đã được giữ lại từ phiên bản trước
    def update(self, employee: Employee, update_data: Dict[str, Any]) -> Employee:
        """Cập nhật các trường được chỉ định trong update_data."""
        for field, value in update_data.items():
            setattr(employee, field, value)
        return employee

    # LƯU Ý: Các hàm get_by_id, get_all, delete đã được BaseRepository xử lý
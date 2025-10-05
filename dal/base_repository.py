from sqlalchemy.orm import Session
from typing import TypeVar, Type, Generic, Optional, List
from sqlalchemy import func

# Định nghĩa TypeVar để chỉ định Entity (Model) mà Repository này quản lý
T = TypeVar("T") 

class BaseRepository(Generic[T]):
    """
    Base Repository Class (Generic Repository) 
    Chứa tất cả các hàm CRUD chung cho mọi Entity.
    """
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        """Lấy một Entity theo ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Lấy tất cả Entity (Hỗ trợ phân trang)"""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def get_count(self) -> int:
        """Đếm tổng số bản ghi"""
        return self.db.query(func.count()).select_from(self.model).scalar()

    def delete(self, entity: T):
        """Xóa một Entity"""
        self.db.delete(entity)

    # Hàm tạo/cập nhật không nằm ở đây vì chúng có thể được tùy chỉnh nhiều
    # Tùy chỉnh: Hàm update cơ bản có thể thêm vào đây
from sqlalchemy import Column, Integer, String
from db.database import Base
from sqlalchemy.orm import relationship

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True) 
    name = Column(String, unique=True, nullable=False)
    # Cập nhật: Thêm trạng thái hoạt động
    status = Column(String, default="Active", nullable=False) 

    # Dùng để kiểm tra khi xóa Department
    employees = relationship("Employee", back_populates="department")
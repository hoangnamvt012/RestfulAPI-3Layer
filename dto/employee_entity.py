from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True) 
    name = Column(String, nullable=False)
    position = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))

    # Cập nhật: Thêm các trường thông tin cá nhân và trạng thái
    phone_number = Column(String(10), nullable=True)
    address = Column(String, nullable=True)
    cccd = Column(String(12), unique=True, nullable=False)
    status = Column(String, default="Active", nullable=False) 

    department = relationship("Department", back_populates="employees")
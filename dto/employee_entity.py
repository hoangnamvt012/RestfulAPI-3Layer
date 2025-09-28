from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    # Cập nhật: Thêm ID Nghiệp vụ
    code = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    position = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department")
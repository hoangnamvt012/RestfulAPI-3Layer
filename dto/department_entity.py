from sqlalchemy import Column, Integer, String
from db.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    # Cập nhật: Thêm ID Nghiệp vụ
    code = Column(String, unique=True, nullable=False, index=True) 
    name = Column(String, unique=True, nullable=False)
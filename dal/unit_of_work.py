from sqlalchemy.orm import Session
from typing import Type, Callable, Optional
from dal.department_repository import DepartmentRepository
from dal.employee_repository import EmployeeRepository
from fastapi import Depends

# ----------------------------------------------------------------------
# Bước 1: Registry cho các Repository (Loại bỏ phụ thuộc cứng)
# ----------------------------------------------------------------------
REPO_REGISTRY = {
    "departments": DepartmentRepository,
    "employees": EmployeeRepository,
    # Thêm các Repository mới vào đây, KHÔNG cần sửa RepositoryGroup
}

class RepositoryGroup:
    """
    Quản lý tập hợp Repository trong một Session.
    Sử dụng __getattr__ để truy cập linh hoạt và Lazy Loading.
    """
    def __init__(self, db: Session):
        self._db = db
        self._cache = {}

    # Phương thức đặc biệt cho phép truy cập self.departments, self.employees
    def __getattr__(self, name: str):
        # Trả về từ cache nếu đã khởi tạo
        if name in self._cache:
            return self._cache[name]

        # Khởi tạo Repository nếu nó tồn tại trong registry
        if name in REPO_REGISTRY:
            RepoClass = REPO_REGISTRY[name]
            repository = RepoClass(self._db) 
            self._cache[name] = repository
            return repository

        raise AttributeError(f"Repository '{name}' not found.")
        
    # Thêm gợi ý kiểu dữ liệu cho IDE
    @property
    def departments(self) -> DepartmentRepository:
        # Giả định thuộc tính tồn tại
        return self.departments
    
    @property
    def employees(self) -> EmployeeRepository:
        # Giả định thuộc tính tồn tại
        return self.employees

# ----------------------------------------------------------------------
# Bước 2: Class UnitOfWork và DI
# ----------------------------------------------------------------------
class UnitOfWork:
    """Quản lý Session DB và Giao dịch (Transaction)"""
    # Sử dụng Callable cho Type Hinting tốt hơn
    def __init__(self, db_session: Callable[..., Session]): 
        self.SessionLocal = db_session
        self.session: Optional[Session] = None
        self.repo: Optional[RepositoryGroup] = None

    def __enter__(self) -> RepositoryGroup:
        """Mở Session và tạo RepositoryGroup."""
        self.session = self.SessionLocal()
        self.repo = RepositoryGroup(self.session)
        return self.repo 

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Xử lý lỗi hoặc đóng Session."""
        if exc_type:
            self.session.rollback()
        self.session.close()

    def commit(self):
        """Thực hiện Commit giao dịch."""
        self.session.commit()

    def refresh(self, instance):
        """Làm mới đối tượng sau commit."""
        self.session.refresh(instance)

# Dependency Injection cho UoW
from db.database import SessionLocal 

def get_uow() -> UnitOfWork:
    # Lấy SessionLocal từ file database.py
    return UnitOfWork(SessionLocal)
from fastapi import HTTPException, status
from dal.unit_of_work import RepositoryGroup # Chỉ dùng RepoGroup để gợi ý kiểu dữ liệu

class DepartmentService:
    def __init__(self, uow: RepositoryGroup):
        # Service giờ chỉ nhận RepositoryGroup (từ UoW)
        self.repo = uow 
        
    # ... (_generate_department_code giữ nguyên)

    def create_department(self, dto):
        # 1. Validation Rule: Tên phòng ban đã tồn tại
        if self.repo.departments.get_by_name(dto.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tên phòng ban '{dto.name}' đã tồn tại."
            )
        
        department_code = self._generate_department_code() 
        
        return self.repo.departments.create(department_code, dto.name, dto.status) # Thêm status

    def update_department(self, department_id: int, dto):
        department = self.get_department_by_id(department_id) # Kiểm tra 404
        
        # 1. Validation Rule: Tên mới có trùng với phòng ban khác không
        if dto.name and self.repo.departments.get_by_name(dto.name) and dto.name != department.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tên phòng ban '{dto.name}' đã tồn tại."
            )

        # Cập nhật (Repo không commit)
        return self.repo.departments.update(department, dto.name, dto.status)
        
    def delete_department(self, department_id: int):
        department = self.get_department_by_id(department_id) # Kiểm tra 404

        # 1. Validation Rule: Không thể xóa Department đang có Employee
        if self.repo.employees.count_by_department(department_id) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Không thể xóa phòng ban này vì vẫn còn nhân viên thuộc về nó."
            )
        
        self.repo.departments.delete(department)
        # Giao dịch sẽ được commit/rollback bởi UoW
        return {"message": f"Department ID {department_id} deleted."}

    # ... (get_department_by_id và list_departments giữ nguyên)
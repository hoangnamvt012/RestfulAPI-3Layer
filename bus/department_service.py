from fastapi import HTTPException, status
from dal.department_repository import DepartmentRepository 
from dto.department_dto import DepartmentCreateDto

class DepartmentService:
    """Xử lý Logic Nghiệp vụ (400, 404) và TẠO ID Nghiệp vụ"""
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository
        
    def _generate_department_code(self) -> str:
        """ID Nghiệp vụ: DEPT-NNNN (Đặt trong Service)"""
        current_count = self.repository.get_count()
        new_id_number = current_count + 1
        return f"DEPT-{new_id_number:04d}" 

    def create_department(self, dto: DepartmentCreateDto):
        # Logic Nghiệp vụ: Xử lý 400 Bad Request
        if self.repository.get_by_name(dto.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tên phòng ban '{dto.name}' đã tồn tại."
            )
        
        department_code = self._generate_department_code() 
        
        return self.repository.create(department_code, dto.name)

    def list_departments(self):
        return self.repository.get_all()
    
    def get_department_by_id(self, department_id: int):
        # Logic Nghiệp vụ: Xử lý 404 Not Found
        department = self.repository.get_by_id(department_id)
        if department is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy phòng ban với ID: {department_id}"
            )
        return department
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from bus.department_service import DepartmentService # Import Class Service
from dal.department_repository import DepartmentRepository # Import Class Repo
from dto.department_dto import DepartmentCreateDto, DepartmentResponseDto
from typing import List

# Hàm Dependency Injection (DI) mới
def get_department_service(db: Session = Depends(get_db)) -> DepartmentService:
    """Tạo Service với Repository được Inject (DIP)"""
    repo = DepartmentRepository(db)
    return DepartmentService(repo)

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post(
    "/", 
    response_model=DepartmentResponseDto, 
    status_code=status.HTTP_201_CREATED # 👈 Status Code 201 chuẩn
)
def create_department(
    dto: DepartmentCreateDto, 
    service: DepartmentService = Depends(get_department_service) # Inject Service
):
    return service.create_department(dto)

@router.get(
    "/{department_id}", 
    response_model=DepartmentResponseDto
)
def get_department(
    department_id: int,
    service: DepartmentService = Depends(get_department_service)
):
    # Service ném 404, Controller bắt và trả về
    return service.get_department_by_id(department_id)

@router.get("/", response_model=List[DepartmentResponseDto])
def list_departments(service: DepartmentService = Depends(get_department_service)):
    return service.list_departments()
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from bus.employee_service import EmployeeService
from dal.employee_repository import EmployeeRepository 
from dal.department_repository import DepartmentRepository 
from dto.employee_dto import EmployeeCreateDto, EmployeeResponseDto
from typing import List

# Hàm Dependency Injection (DI) mới
def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    """Tạo Service với cả 2 Repository được Inject (DIP)"""
    emp_repo = EmployeeRepository(db)
    dept_repo = DepartmentRepository(db) 
    return EmployeeService(emp_repo, dept_repo)

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post(
    "/", 
    response_model=EmployeeResponseDto,
    status_code=status.HTTP_201_CREATED # 👈 Status Code 201 chuẩn
)
def create_employee(
    dto: EmployeeCreateDto, 
    service: EmployeeService = Depends(get_employee_service) # Inject Service
):
    return service.create_employee(dto)

@router.get(
    "/{employee_id}", 
    response_model=EmployeeResponseDto
)
def get_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service)
):
    # Service ném 404, Controller bắt và trả về
    return service.get_employee_by_id(employee_id)

@router.get("/", response_model=List[EmployeeResponseDto])
def list_employees(service: EmployeeService = Depends(get_employee_service)):
    return service.list_employees()
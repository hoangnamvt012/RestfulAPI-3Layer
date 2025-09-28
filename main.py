from fastapi import FastAPI
from db.database import Base, engine
from presentation import department_controller, employee_controller

# Tạo bảng DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Company API")

# Gắn router
app.include_router(department_controller.router)
app.include_router(employee_controller.router)

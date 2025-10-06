# File: exceptions.py

from typing import Dict

# BẢNG ÁNH XẠ: Mã lỗi nghiệp vụ nội bộ -> Mã HTTP Status Code chuẩn
ERROR_MAPPING: Dict[int, int] = {
    # 400x: Lỗi Not Found (404)
    4001: 404,  # NOT_FOUND (Chung cho Employee/Department)
    
    # 401x: Lỗi Bad Request (400)
    4011: 400,  # BAD_REQUEST (Khóa ngoại không hợp lệ)
    4012: 400,  # BAD_REQUEST (Không thể xóa vì còn liên kết)
    
    # 409x: Lỗi Conflict (409)
    4091: 409,  # CONFLICT (Tên/CCCD đã tồn tại)
    
    # 403x: Lỗi Forbidden
    4031: 403,  # FORBIDDEN (Thiếu quyền hạn)
}

# BASE EXCEPTION: Tầng BUS chỉ ném Exception này với mã lỗi nội bộ
class APIException(Exception):
    def __init__(self, error_code: int, detail: str = None):
        if error_code not in ERROR_MAPPING:
            raise ValueError(f"Invalid internal error code: {error_code}") 
            
        self.error_code = error_code
        self.detail = detail if detail else "A business logic error occurred."
        super().__init__(detail)

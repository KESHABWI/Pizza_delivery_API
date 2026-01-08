from pydantic import BaseModel
from typing import Optional 
class SignUpModel(BaseModel):
    id: Optional[int]=None
    username: str
    email: str
    password: str
    is_staff: Optional[bool] =False
    is_active: Optional[bool]=True

    class Config:
         from_attributes = True
         json_schema_extra = {
            "example": {
                "username": "Keshab Kamal",
                "email": "keshabkamal@example.com",
                "password": "secret123",
                "is_staff": False,
                "is_active": True
            }  
        }  
    


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int]=None
    quantity: int
    pizza_size: Optional[str]="SMALL"
    order_status: Optional[str]="PENDING"
    user_id: Optional[int]=None

    class Config:
         from_attributes = True
         json_schema_extra = {
            "example": {
                "quantity": 2,
                "pizza_size": "MEDIUM"
            }  
        }
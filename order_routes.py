from fastapi import APIRouter,Depends ,status, HTTPException
from dependencies.auth import get_current_user
from models import User,Order
from schemas import OrderModel
from database import SessionLocal, engine
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(prefix="/orders", tags=["orders"])

session = SessionLocal(bind=engine)


@order_router.get('/')
async def hello(current_user: str = Depends(get_current_user)):
     return {"message": f"Hello {current_user}"}  

@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, current_user: str = Depends(get_current_user)):
    user=session.query(User).filter(User.username == current_user).first()
    new_order = Order(
        quantity=order.quantity,
        pizza_size=order.pizza_size,
    )
    new_order.user = user
    session.add(new_order)
    session.commit()
    response={
         "pizza_size": new_order.pizza_size,
         "order_status": new_order.order_status,
         "quantity": new_order.quantity,
         "user_id": new_order.user_id,
         "message": "Order placed successfully"
    }
    return jsonable_encoder(response)
    

@order_router.get('/orders',status_code=status.HTTP_200_OK)
async def list_all_orders(current_user: str = Depends(get_current_user)):
    user=session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
          orders=session.query(Order).all()
          return jsonable_encoder(orders)
    raise HTTPException(status_code=403, detail="Not authorized to view all orders.You are not staff member")


@order_router.get('/orders/{order_id}',status_code=status.HTTP_200_OK)
async def get_order_by_id(order_id: int, current_user: str = Depends(get_current_user)):
    user=session.query(User).filter(User.username == current_user).first()
    
    
    if user.is_staff:
        order = session.query(Order).filter(Order.id == order_id).first()
        if not order:
         raise HTTPException(status_code=404, detail="Order not found")

        return jsonable_encoder(order)
    raise HTTPException(status_code=403, detail="Not authorized to view this order")
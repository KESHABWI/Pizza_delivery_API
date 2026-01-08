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
     """
        ## A sample hello {current user}
        This return hello username
     """
     return {"message": f"Hello {current_user}"}  

@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, current_user: str = Depends(get_current_user)):
    """
        ## Place an order
        This endpoint allows an authenticated user to place a pizza order.
        - **quantity**: Number of pizzas to order (integer).
        - **pizza_size**: Size of the pizza (string, default is "SMALL").
    """
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
    """
        ## List all orders
        This endpoint allows staff users to view all pizza orders in the system.
        Only users with staff privileges can access this endpoint.
    """
    user=session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
          orders=session.query(Order).all()
          return jsonable_encoder(orders)
    raise HTTPException(status_code=403, detail="Not authorized to view all orders.You are not staff member")


@order_router.get('/orders/{order_id}',status_code=status.HTTP_200_OK)
async def get_order_by_id(order_id: int, current_user: str = Depends(get_current_user)):
    """
        ## Get order by ID
        This endpoint allows staff users to retrieve details of a specific pizza order by its ID.
        Only users with staff privileges can access this endpoint.
    """
    user=session.query(User).filter(User.username == current_user).first()
    
    
    if user.is_staff:
        order = session.query(Order).filter(Order.id == order_id).first()
        if not order:
         raise HTTPException(status_code=404, detail="Order not found")

        return jsonable_encoder(order)
    raise HTTPException(status_code=403, detail="Not authorized to view this order")


@order_router.get('/user/orders',status_code=status.HTTP_200_OK)
async def get_user_orders(current_user: str = Depends(get_current_user)):
    """
        ## Get user's orders
        This endpoint allows an authenticated user to retrieve all their pizza orders.
    """
    user=session.query(User).filter(User.username == current_user).first()
    orders=session.query(Order).filter(Order.user_id == user.id).all()
    return jsonable_encoder(orders)

@order_router.get('/user/orders/{order_id}',status_code=status.HTTP_200_OK)
async def get_user_order_by_id(order_id: int, current_user: str = Depends(get_current_user)):
    """
        ## Get user's order by ID
        This endpoint allows an authenticated user to retrieve details of a specific pizza order by its ID.
    """
    user=session.query(User).filter(User.username == current_user).first()
    order=session.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not order:
         raise HTTPException(status_code=404, detail="Order not found")
    return jsonable_encoder(order)

@order_router.put('/order/update/{order_id}',status_code=status.HTTP_200_OK)
async def update_order(order_id: int, updated_order: OrderModel, current_user: str = Depends(get_current_user)):
    """
        ## Update an order
        This endpoint allows an authenticated user to update the details of their pizza order.
        - **quantity**: Updated number of pizzas (integer).
        - **pizza_size**: Updated size of the pizza (string).
    """
    order_to_update=session.query(Order).filter(Order.id == order_id).first()
    if not order_to_update:
         raise HTTPException(status_code=404, detail="Order not found")

    order_to_update.quantity = updated_order.quantity
    order_to_update.pizza_size = updated_order.pizza_size
    session.commit()

    return jsonable_encoder(order_to_update)

@order_router.delete('/order/delete/{order_id}',status_code=status.HTTP_200_OK)
async def delete_order(order_id: int, current_user: str = Depends(get_current_user)): 
    """
        ## Delete an order
        This endpoint allows an authenticated user to delete their pizza order by its ID.
    """  
    order_to_delete=session.query(Order).filter(Order.id == order_id).first()
    if not order_to_delete:
         raise HTTPException(status_code=404, detail="Order not found")

    session.delete(order_to_delete)
    session.commit()

    return {"message": "Order deleted successfully"}
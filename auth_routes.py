from fastapi import APIRouter, status, Depends, HTTPException
from database import SessionLocal, engine
from schemas import SignUpModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder

from utils.jwt import create_access_token, create_refresh_token, verify_token
from dependencies.auth import get_current_user

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


session = SessionLocal(bind=engine)


@auth_router.get("/")
async def hello(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}"}


# ---------------- SIGNUP ----------------
@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):

    if session.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    if session.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()

    return jsonable_encoder(new_user)


# ---------------- LOGIN ----------------
@auth_router.post("/login",status_code=200)
async def login(user:LoginModel):

    db_user=session.query(User).filter(User.username==user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token=create_access_token({"sub": db_user.username})
        refresh_token=create_refresh_token({"sub": db_user.username})

        response={
            "access":access_token,
            "refresh":refresh_token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid Username Or Password"
    )


# ---------------- REFRESH ----------------
@auth_router.get("/refresh")
async def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token, "refresh")

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token({"sub": payload["sub"]})
    return {"access": access_token}
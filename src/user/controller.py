from anyio import current_time
from fastapi import HTTPException,status,Request
from src.user.dtos import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime, timedelta
import jwt
from jwt import InvalidTokenError

password_hash = PasswordHash.recommended()


def get_password_hash(password):
  return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
  return password_hash.verify(plain_password, hashed_password)

def register(body: UserSchema, db: Session):
  is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
  if is_user:
    raise HTTPException(status_code=400, detail="Username already exists.")
  
  is_email = db.query(UserModel).filter(UserModel.email == body.email).first()
  if is_email:
    raise HTTPException(status_code=400, detail="Email Address already exists.")

  hash_password = get_password_hash(body.password)
  new_user = UserModel(
    name=body.name, 
    username=body.username, 
    hash_password=hash_password,  
    email=body.email
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user

def login_user(body: LoginSchema, db: Session):
  user = db.query(UserModel).filter(UserModel.username == body.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username.")
  
  if not verify_password(body.password, user.hash_password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password.")

  # exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
  exp_time = datetime.now() + timedelta(seconds = 20)
  print(exp_time)
  token = jwt.encode({"_id": user.id,"exp": exp_time.timestamp()}, settings.SECRET_KEY, settings.ALGORITHM)

  return {"token": token}

def is_authenticated(request:Request,db:Session):
  try:
      token = request.headers.get("Authorization")
      if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing.")
      token = token.split(" ")[-1]

      data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
      # user_id = data.get("_id")
      # exp_time = int(data.get("exp"))

      # current_time = datetime.now().timestamp()
      # print(exp_time - current_time)

      # if current_time > exp_time:
      #   raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")

      user = db.query(UserModel).filter(UserModel.id == user_id).first()
      if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")

      return user
  except InvalidTokenError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are a=unauthorized.")

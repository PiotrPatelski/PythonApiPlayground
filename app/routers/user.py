from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, utils
from ..database import dbmodels
from app.database.dbhandle import get_database

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[schemas.UserPublicDetails])
def get_users(database: Session = Depends(get_database)):
    users = database.query(dbmodels.User).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserPublicDetails)
def create_user(user: schemas.UserCreate, database: Session = Depends(get_database)):
    hashed_password = utils.encrypt(user.password)
    user.password = hashed_password

    new_user = dbmodels.User(**user.model_dump())
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserPublicDetails)
def get_user(id: int, database: Session = Depends(get_database)):
    user = database.query(dbmodels.User).filter(dbmodels.User.id == id).first()
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"user with id: {id} does not exist!")
    return user
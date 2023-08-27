from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.dbhandle import get_database
from .. import schemas, utils, oauth2
from ..database import dbmodels

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_database)):

    user = database.query(dbmodels.User).filter(
        dbmodels.User.email == user_credentials.username).first()
    if user is None or utils.verify(user_credentials.password, user.password) is not True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials!")
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
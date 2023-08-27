from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import schemas, oauth2
from ..database import dbmodels
from app.database.dbhandle import get_database

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# @router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(
        database: Session = Depends(get_database),
        current_user: dbmodels.User = Depends(oauth2.get_current_user),
        amount: int = 10,
        skip: int = 0,
        search: Optional[str] = ""):
    results = database.query(dbmodels.Post, func.count(dbmodels.Vote.post_id).label("votes"))\
        .join(dbmodels.Vote, dbmodels.Vote.post_id == dbmodels.Post.id, isouter=True)\
        .group_by(dbmodels.Post.id) \
        .filter(dbmodels.Post.title.contains(search)) \
        .limit(amount) \
        .offset(skip).all()
    posts_list = list(map(lambda x: x._mapping, results))
    return posts_list


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostContent)
def create_post(
        post: schemas.PostCreate,
        database: Session = Depends(get_database),
        current_user: dbmodels.User = Depends(oauth2.get_current_user)):
    new_post = dbmodels.Post(owner_id=current_user.id, **post.model_dump())
    database.add(new_post)
    database.commit()
    database.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(
        id: int,
        database: Session = Depends(get_database),
        current_user: dbmodels.User = Depends(oauth2.get_current_user)):
    post = results = database.query(dbmodels.Post, func.count(dbmodels.Vote.post_id).label("votes"))\
        .join(dbmodels.Vote, dbmodels.Vote.post_id == dbmodels.Post.id, isouter=True)\
        .group_by(dbmodels.Post.id)\
        .filter(dbmodels.Post.id == id)\
        .first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist!")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        id: int,
        database: Session = Depends(get_database),
        current_user: dbmodels.User = Depends(oauth2.get_current_user)):
    query_response = database.query(dbmodels.Post).filter(dbmodels.Post.id == id)
    post = query_response.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist!")
    elif post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"unauthorized action!")
    query_response.delete(synchronize_session=False)
    database.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostContent)
def update_post(
        id: int,
        updated_post: schemas.PostCreate,
        database: Session = Depends(get_database),
        current_user: dbmodels.User = Depends(oauth2.get_current_user)):
    query_response = database.query(dbmodels.Post).filter(dbmodels.Post.id == id)
    post = query_response.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist!")
    elif post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"unauthorized action!")
    query_response.update(updated_post.model_dump(), synchronize_session=False)
    database.commit()
    return query_response.first()

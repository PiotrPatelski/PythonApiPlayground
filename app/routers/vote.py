from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import schemas, oauth2
from ..database import dbmodels
from app.database.dbhandle import get_database

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
         current_user: dbmodels.User = Depends(oauth2.get_current_user),
         database: Session = Depends(get_database)):

    post = database.query(dbmodels.Post).filter(dbmodels.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {vote.post_id}, does not exist!")
    vote_query = database.query(dbmodels.Vote).filter(
        dbmodels.Vote.post_id == vote.post_id, dbmodels.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if(vote.like_ind is True):
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted for this "
                       f"post {vote.post_id}")
        else:
            new_vote = dbmodels.Vote(post_id = vote.post_id, user_id = current_user.id)
            database.add(new_vote)
            database.commit()
            return {"message": "Voted successfully!"}
    else:
        if found_vote:
            vote_query.delete(synchronize_session=False)
            database.commit()
            return {"message": "Vote removed successfully!"}
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot remove vote from post you did not vote for!")

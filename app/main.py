
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import dbmodels
from app.database.dbhandle import engine
from app.routers import post, user, authentication, vote
from app.config import settings

app = FastAPI()

origins = ["*"]# '*' to access for every website

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Pioter api!"}



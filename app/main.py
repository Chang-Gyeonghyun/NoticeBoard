from fastapi import FastAPI
from app.api.v1.routers import user, posts, comments

app = FastAPI()

app.include_router(user.router)
app.include_router(posts.router)
app.include_router(comments.router)
from fastapi import FastAPI, HTTPException, Request
from fastapi.params import Depends
from fastapi.templating import Jinja2Templates
from typing import List
from sqlalchemy.orm import Session
import models
from models import Post
from schemas import TextPostSchema, SubmitPostSchema, ListPostsSchema
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.parent_id == None).all()
    for i in range(len(posts)):
        posts[i].replies = db.query(Post).filter(Post.parent_id == posts[i].id).all()
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})


@app.post("/post/", response_model=int, status_code=201)
def post_text_post(text_post: SubmitPostSchema, db: Session = Depends(get_db)):
    db_post = Post(content=text_post.content, parent_id=None)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post.id


@app.get("/post/{post_id}", response_model=TextPostSchema)
def get_text_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id, Post.parent_id == None).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/post/{post_id}/reply", status_code=201)
def reply_to_text_post(post_id: int, reply: SubmitPostSchema, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_reply = Post(content=reply.content, parent_id=post_id)
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    return {"success": "Reply added successfully"}


@app.get("/posts/", response_model=List[ListPostsSchema])
def get_all_posts(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.parent_id == None).offset(offset).limit(limit).all()
    for i in range(len(posts)):
        posts[i].replies = db.query(Post).filter(Post.parent_id == posts[i].id).all()
    return posts

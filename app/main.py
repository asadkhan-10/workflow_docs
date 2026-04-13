# app/main.py
from .routers import users, workflows, auth

from .database import Base, engine
from . import models
from fastapi import FastAPI

# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(workflows.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {
        "message": "hello from Workflow Docs API, and deployed succesfully on aws"
    }

from fastapi import FastAPI
from src.routers import task
from src.routers import user
from src.database import engine, Base
from src.model import Task
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to the Task Manager API"}

app.include_router(task.router)
app.include_router(user.router)
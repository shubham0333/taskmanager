from fastapi import APIRouter, Depends, HTTPException, status
from src.routers.user import get_current_user
from src.schemas import TaskCreate
from src.database import get_db
from src.model.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/create_task")
def create_task(task_data: TaskCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    new_task = Task(**task_data.model_dump(), user_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/get-tasks")
def get_tasks(db=Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Task).filter(Task.user_id == current_user.id).order_by(Task.id.desc()).all()


@router.get("/get-task/{task_id}")
def get_task(task_id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task


@router.put("/update-task/{task_id}")
def update_task(task_id: int, task_data: TaskCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db_task.title = task_data.title
    db_task.description = task_data.description
    db_task.completed = task_data.completed

    db.commit()
    db.refresh(db_task)

    return db_task


@router.delete("/delete-task/{task_id}")
def delete_task(task_id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(db_task)
    db.commit()

    return {"message": "Task deleted successfully"}

from fastapi import APIRouter, Depends
from src.routers.user import get_current_user
from src.schemas import TaskCreate
from src.database import get_db
from src.model.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/create_task")
def create_task(task_data: TaskCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user:
        return {"message": "Unauthorized"}

    new_task = Task(**task_data.model_dump(), user_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/get-tasks")
def get_tasks(db=Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user:
        return {"message": "Unauthorized"}

    try:
        tasks = db.query(Task).filter(Task.user_id == current_user.id).order_by(Task.id.desc()).all()
        return tasks
    except Exception as e:
        print(f"Error occurred while fetching tasks: {e}")
        return []


@router.get("/get-task/{task_id}")
def get_task(task_id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user:
        return {"message": "Unauthorized"}

    try:
        db_task = db.query(Task).filter(Task.id == task_id).first()
        if db_task is None:
            return {"message": "Task not found"}
        if db_task.user_id != current_user.id:
            return {"message": "Unauthorized"}
        return db_task
    except Exception as e:
        print(f"Error occurred while fetching the task: {e}")
        return {"message": "An error occurred while fetching the task"}


@router.put("/update-task/{task_id}")
def update_task(task_id: int, task_data: TaskCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user:
        return {"message": "Unauthorized"}

    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        return {"message": "Task not found"}
    if db_task.user_id != current_user.id:
        return {"message": "Unauthorized"}

    db_task.title = task_data.title
    db_task.description = task_data.description
    db_task.completed = task_data.completed

    db.commit()
    db.refresh(db_task)

    return db_task


@router.delete("/delete-task/{task_id}")
def delete_task(task_id: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user:
        return {"message": "Unauthorized"}

    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        return {"message": "Task not found"}
    if db_task.user_id != current_user.id:
        return {"message": "Unauthorized"}

    db.delete(db_task)
    db.commit()

    return {"message": "Task deleted successfully"}
from fastapi import APIRouter, Depends, HTTPException, status
from src.database import get_db
from src.schemas import UserCreate 
from src.model.user import User
from src.security import auth
from fastapi.security import OAuth2PasswordRequestForm

router =APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
def create_user(user: UserCreate, db=Depends(get_db)):

    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    new_user = User(username=user.username, password=auth.hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username,}


@router.post("/login")
def login_user(user: UserCreate, db=Depends(get_db)):

    existing_user = db.query(User).filter(User.username == user.username).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not auth.verify_password(user.password, existing_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    access_token = auth.create_access_token(data={"sub": existing_user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    existing_user = db.query(User).filter(User.username == form_data.username).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not auth.verify_password(form_data.password, existing_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": existing_user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
def verify_token(token: str):
    try:
        payload = auth.jwt.decode(token, auth.settings.secret_key, algorithms=[auth.settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except auth.JWTError:
        return None
    
def get_current_user(token: str = Depends(auth.oauth2_scheme), db=Depends(get_db)):
    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


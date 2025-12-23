from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from . import models, schemas, database, crud, auth
import uvicorn
import os
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from ml.inference import ner_infer

app = FastAPI(title="DMS Showcase Advanced")

# CORS middleware - for demo we allow all origins. For public demo restrict origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Health endpoint (used by tests/monitoring)
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def startup():
    # Alembic handles migrations in production; seed/migrations triggered by entrypoint
    pass

async def get_db():
    async for s in database.get_session():
        yield s

@app.post("/register", response_model=schemas.UserOut)
async def register(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    user = await crud.create_user(db, email=user_in.email, password=user_in.password, full_name=user_in.full_name)
    if user is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    sub = auth.decode_token(token)
    if sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return int(sub)

@app.post("/icrs", response_model=schemas.ICSROut)
async def create_icrs(ic: schemas.ICSRIn, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    icsr = await crud.create_icsr(db, ic.title, ic.narrative, created_by_id=user_id)
    return icsr

@app.get("/icrs", response_model=List[schemas.ICSROut])
async def get_icrs(db: AsyncSession = Depends(get_db)):
    return await crud.list_icrs(db)

@app.post("/ml/ner")
async def ml_ner(payload: dict):
    if "text" not in payload:
        raise HTTPException(status_code=400, detail="Provide 'text'")
    ents = ner_infer(payload["text"])
    return {"entities": ents}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=True)
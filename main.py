from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Annotated
import models as models
from database import SessionLocal,engine
from sqlalchemy.orm import Session


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)

class Counter(BaseModel):
    limit_value: int

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/counter/")
async def get_counter(db: Session = Depends(get_db)):
    counter = db.query(models.Counter).first()
    return {"limit_value": counter.limit_value if counter else 10}

@app.put("/counter/")
async def update_counter(update_data: Counter, db: Session = Depends(get_db)):
    counter = db.query(models.Counter).first()
    if not counter:
        counter = models.Counter(limit_value=update_data.limit_value)
        db.add(counter)
    else:
        counter.limit_value = update_data.limit_value
    db.commit()
    return {"limit_value": update_data.limit_value}

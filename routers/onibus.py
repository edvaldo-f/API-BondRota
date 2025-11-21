from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/onibus",
    tags=["Onibus"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.OnibusResponse)
def create_onibus(onibus: schemas.OnibusCreate, db: Session = Depends(get_db)):
    if db.query(models.Onibus).filter(models.Onibus.placa == onibus.placa).first():
        raise HTTPException(status_code=400, detail="Placa já cadastrada")

    new_onibus = models.Onibus(**onibus.dict())
    db.add(new_onibus)
    db.commit()
    db.refresh(new_onibus)
    return new_onibus

@router.get("/", response_model=List[schemas.OnibusResponse])
def read_all_onibus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    onibus_list = db.query(models.Onibus).offset(skip).limit(limit).all()
    return onibus_list

@router.get("/{onibus_id}", response_model=schemas.OnibusResponse)
def read_onibus(onibus_id: int, db: Session = Depends(get_db)):
    onibus = db.query(models.Onibus).filter(models.Onibus.id_onibus == onibus_id).first()
    if not onibus:
        raise HTTPException(status_code=404, detail="Ônibus não encontrado")
    return onibus

@router.put("/{onibus_id}", response_model=schemas.OnibusResponse)
def update_onibus(onibus_id: int, onibus_update: schemas.OnibusCreate, db: Session = Depends(get_db)):
    db_onibus = db.query(models.Onibus).filter(models.Onibus.id_onibus == onibus_id).first()
    if not db_onibus:
        raise HTTPException(status_code=404, detail="Ônibus não encontrado")
    
    # Método prático para atualizar todos os campos
    for key, value in onibus_update.dict().items():
        setattr(db_onibus, key, value)

    db.commit()
    db.refresh(db_onibus)
    return db_onibus

@router.delete("/{onibus_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_onibus(onibus_id: int, db: Session = Depends(get_db)):
    db_onibus = db.query(models.Onibus).filter(models.Onibus.id_onibus == onibus_id).first()
    if not db_onibus:
        raise HTTPException(status_code=404, detail="Ônibus não encontrado")
    
    db.delete(db_onibus)
    db.commit()
    return None
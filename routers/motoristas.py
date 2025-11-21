from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/motoristas",
    tags=["Motoristas"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MotoristaResponse)
def create_motorista(motorista: schemas.MotoristaCreate, db: Session = Depends(get_db)):
    if db.query(models.Motorista).filter(models.Motorista.cpf == motorista.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    new_motorista = models.Motorista(**motorista.dict())
    db.add(new_motorista)
    db.commit()
    db.refresh(new_motorista)
    return new_motorista

@router.get("/", response_model=List[schemas.MotoristaResponse])
def read_motoristas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    motoristas = db.query(models.Motorista).offset(skip).limit(limit).all()
    return motoristas

@router.get("/{motorista_id}", response_model=schemas.MotoristaResponse)
def read_motorista(motorista_id: int, db: Session = Depends(get_db)):
    motorista = db.query(models.Motorista).filter(models.Motorista.id_motorista == motorista_id).first()
    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    return motorista

@router.put("/{motorista_id}", response_model=schemas.MotoristaResponse)
def update_motorista(motorista_id: int, motorista_update: schemas.MotoristaCreate, db: Session = Depends(get_db)):
    db_motorista = db.query(models.Motorista).filter(models.Motorista.id_motorista == motorista_id).first()
    if not db_motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    
    db_motorista.nome = motorista_update.nome
    db_motorista.cpf = motorista_update.cpf
    db_motorista.telefone = motorista_update.telefone
    db_motorista.data_de_nascimento = motorista_update.data_de_nascimento
    
    db.commit()
    db.refresh(db_motorista)
    return db_motorista

@router.delete("/{motorista_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_motorista(motorista_id: int, db: Session = Depends(get_db)):
    db_motorista = db.query(models.Motorista).filter(models.Motorista.id_motorista == motorista_id).first()
    if not db_motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    
    db.delete(db_motorista)
    db.commit()
    return None
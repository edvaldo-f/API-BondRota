from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/rotas",
    tags=["Rotas"]
)

# CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RotaResponse)
def create_rota(rota: schemas.RotaCreate, db: Session = Depends(get_db)):
    new_rota = models.Rota(**rota.dict())
    db.add(new_rota)
    db.commit()
    db.refresh(new_rota)
    return new_rota

# READ ALL
@router.get("/", response_model=List[schemas.RotaResponse])
def read_rotas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rotas = db.query(models.Rota).offset(skip).limit(limit).all()
    return rotas

# READ ONE
@router.get("/{rota_id}", response_model=schemas.RotaResponse)
def read_rota(rota_id: int, db: Session = Depends(get_db)):
    rota = db.query(models.Rota).filter(models.Rota.id_rota == rota_id).first()
    if not rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    return rota

# UPDATE
@router.put("/{rota_id}", response_model=schemas.RotaResponse)
def update_rota(rota_id: int, rota_update: schemas.RotaCreate, db: Session = Depends(get_db)):
    db_rota = db.query(models.Rota).filter(models.Rota.id_rota == rota_id).first()
    if not db_rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    
    # Atualiza os campos
    db_rota.nome = rota_update.nome
    db_rota.pontos = rota_update.pontos
    db_rota.quantidade_total = rota_update.quantidade_total
    db_rota.quantidade_diaria = rota_update.quantidade_diaria
    
    db.commit()
    db.refresh(db_rota)
    return db_rota

# DELETE
@router.delete("/{rota_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rota(rota_id: int, db: Session = Depends(get_db)):
    db_rota = db.query(models.Rota).filter(models.Rota.id_rota == rota_id).first()
    if not db_rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    
    db.delete(db_rota)
    db.commit()
    return None
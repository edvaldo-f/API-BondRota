from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Motorista
from schemas import Motorista as MotoristaSchema, MotoristaCreate, MotoristaUpdate

router = APIRouter(prefix="/motoristas", tags=["motoristas"])

@router.get("/", response_model=list[MotoristaSchema])
def listar_motoristas(db: Session = Depends(get_db)):
    """Listar todos os motoristas"""
    return db.query(Motorista).all()

@router.get("/{motorista_id}", response_model=MotoristaSchema)
def obter_motorista(motorista_id: int, db: Session = Depends(get_db)):
    """Obter um motorista específico"""
    motorista = db.query(Motorista).filter(Motorista.id_motorista == motorista_id).first()
    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    return motorista

@router.post("/", response_model=MotoristaSchema)
def criar_motorista(motorista: MotoristaCreate, db: Session = Depends(get_db)):
    """Criar um novo motorista"""
    db_motorista = Motorista(**motorista.dict())
    db.add(db_motorista)
    db.commit()
    db.refresh(db_motorista)
    return db_motorista

@router.put("/{motorista_id}", response_model=MotoristaSchema)
def atualizar_motorista(motorista_id: int, motorista: MotoristaUpdate, db: Session = Depends(get_db)):
    """Atualizar um motorista"""
    db_motorista = db.query(Motorista).filter(Motorista.id_motorista == motorista_id).first()
    if not db_motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    
    for key, value in motorista.dict(exclude_unset=True).items():
        setattr(db_motorista, key, value)
    
    db.commit()
    db.refresh(db_motorista)
    return db_motorista

@router.delete("/{motorista_id}")
def deletar_motorista(motorista_id: int, db: Session = Depends(get_db)):
    """Deletar um motorista"""
    db_motorista = db.query(Motorista).filter(Motorista.id_motorista == motorista_id).first()
    if not db_motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    db.delete(db_motorista)
    db.commit()
    return {"message": "Motorista deletado com sucesso"}

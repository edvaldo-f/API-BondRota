from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Onibus
from schemas import Onibus as OnibusSchema, OnibusCreate, OnibusUpdate

router = APIRouter(prefix="/onibus", tags=["onibus"])

@router.get("/", response_model=list[OnibusSchema])
def listar_onibus(db: Session = Depends(get_db)):
    """Listar todos os onibus"""
    return db.query(Onibus).all()

@router.get("/{onibus_id}", response_model=OnibusSchema)
def obter_onibus(onibus_id: int, db: Session = Depends(get_db)):
    """Obter um onibus específico"""
    onibus = db.query(Onibus).filter(Onibus.id_onibus == onibus_id).first()
    if not onibus:
        raise HTTPException(status_code=404, detail="Onibus não encontrado")
    return onibus

@router.post("/", response_model=OnibusSchema)
def criar_onibus(onibus: OnibusCreate, db: Session = Depends(get_db)):
    """Criar um novo onibus"""
    db_onibus = Onibus(**onibus.dict())
    db.add(db_onibus)
    db.commit()
    db.refresh(db_onibus)
    return db_onibus

@router.put("/{onibus_id}", response_model=OnibusSchema)
def atualizar_onibus(onibus_id: int, onibus: OnibusUpdate, db: Session = Depends(get_db)):
    """Atualizar um onibus"""
    db_onibus = db.query(Onibus).filter(Onibus.id_onibus == onibus_id).first()
    if not db_onibus:
        raise HTTPException(status_code=404, detail="Onibus não encontrado")
    
    for key, value in onibus.dict(exclude_unset=True).items():
        setattr(db_onibus, key, value)
    
    db.commit()
    db.refresh(db_onibus)
    return db_onibus

@router.delete("/{onibus_id}")
def deletar_onibus(onibus_id: int, db: Session = Depends(get_db)):
    """Deletar um onibus"""
    db_onibus = db.query(Onibus).filter(Onibus.id_onibus == onibus_id).first()
    if not db_onibus:
        raise HTTPException(status_code=404, detail="Onibus não encontrado")
    db.delete(db_onibus)
    db.commit()
    return {"message": "Onibus deletado com sucesso"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Rota
from schemas import Rota as RotaSchema, RotaCreate, RotaUpdate

router = APIRouter(prefix="/rotas", tags=["rotas"])

@router.get("/", response_model=list[RotaSchema])
def listar_rotas(db: Session = Depends(get_db)):
    """Listar todas as rotas"""
    return db.query(Rota).all()

@router.get("/{rota_id}", response_model=RotaSchema)
def obter_rota(rota_id: int, db: Session = Depends(get_db)):
    """Obter uma rota específico"""
    rota = db.query(Rota).filter(Rota.id_rota == rota_id).first()
    if not rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    return rota

@router.post("/", response_model=RotaSchema)
def criar_rota(rota: RotaCreate, db: Session = Depends(get_db)):
    """Criar uma nova rota"""
    db_rota = Rota(**rota.dict())
    db.add(db_rota)
    db.commit()
    db.refresh(db_rota)
    return db_rota

@router.put("/{rota_id}", response_model=RotaSchema)
def atualizar_rota(rota_id: int, rota: RotaUpdate, db: Session = Depends(get_db)):
    """Atualizar uma rota"""
    db_rota = db.query(Rota).filter(Rota.id_rota == rota_id).first()
    if not db_rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    
    for key, value in rota.dict(exclude_unset=True).items():
        setattr(db_rota, key, value)
    
    db.commit()
    db.refresh(db_rota)
    return db_rota

@router.delete("/{rota_id}")
def deletar_rota(rota_id: int, db: Session = Depends(get_db)):
    """Deletar uma rota"""
    db_rota = db.query(Rota).filter(Rota.id_rota == rota_id).first()
    if not db_rota:
        raise HTTPException(status_code=404, detail="Rota não encontrada")
    db.delete(db_rota)
    db.commit()
    return {"message": "Rota deletada com sucesso"}
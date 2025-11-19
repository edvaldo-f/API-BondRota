from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Aluno
from schemas import Aluno as AlunoSchema, AlunoCreate, AlunoUpdate

router = APIRouter(prefix="/alunos", tags=["alunos"])

@router.get("/", response_model=list[AlunoSchema])
def listar_alunos(db: Session = Depends(get_db)):
    """Listar todos os alunos"""
    return db.query(Aluno).all()

@router.get("/{aluno_id}", response_model=AlunoSchema)
def obter_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """Obter um aluno específico"""
    aluno = db.query(Aluno).filter(Aluno.id_aluno == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.post("/", response_model=AlunoSchema)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    """Criar um novo aluno"""
    db_aluno = Aluno(**aluno.dict())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

@router.put("/{aluno_id}", response_model=AlunoSchema)
def atualizar_aluno(aluno_id: int, aluno: AlunoUpdate, db: Session = Depends(get_db)):
    """Atualizar um aluno"""
    db_aluno = db.query(Aluno).filter(Aluno.id_aluno == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    for key, value in aluno.dict(exclude_unset=True).items():
        setattr(db_aluno, key, value)
    
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

@router.delete("/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """Deletar um aluno"""
    db_aluno = db.query(Aluno).filter(Aluno.id_aluno == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(db_aluno)
    db.commit()
    return {"message": "Aluno deletado com sucesso"}

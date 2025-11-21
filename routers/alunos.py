from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AlunoResponse)
def create_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    # Verifica CPF duplicado
    if db.query(models.Aluno).filter(models.Aluno.cpf == aluno.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
        
    new_aluno = models.Aluno(**aluno.dict())
    db.add(new_aluno)
    db.commit()
    db.refresh(new_aluno)
    return new_aluno

@router.get("/", response_model=List[schemas.AlunoResponse])
def read_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alunos = db.query(models.Aluno).offset(skip).limit(limit).all()
    return alunos

@router.get("/{aluno_id}", response_model=schemas.AlunoResponse)
def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(models.Aluno).filter(models.Aluno.id_aluno == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.put("/{aluno_id}", response_model=schemas.AlunoResponse)
def update_aluno(aluno_id: int, aluno_update: schemas.AlunoCreate, db: Session = Depends(get_db)):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id_aluno == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    for key, value in aluno_update.dict().items():
        setattr(db_aluno, key, value)

    db.commit()
    db.refresh(db_aluno)
    return db_aluno

@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id_aluno == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    db.delete(db_aluno)
    db.commit()
    return None
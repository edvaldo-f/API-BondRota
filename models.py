from sqlalchemy import Column, Integer, String, VARCHAR, Boolean, ForeignKey, CheckConstraint, Date, CHAR, Text
from sqlalchemy.orm import relationship
from database import Base

#Modelos das tabelas

class Aluno(Base):
    __tablename__ = "alunos"
    id_aluno = Column(Integer, primary_key=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    instituicao_de_ensino = Column(VARCHAR(150), nullable=False)
    curso = Column(VARCHAR(100), nullable=False)
    data_de_nascimento = Column(Date)
    cpf = Column(CHAR(11), unique=True, nullable=False)
    turno = Column(VARCHAR(10), nullable=False)
    id_rota = relationship("Rota", secondary="alunos_rotas", back_populates="alunos")

class Motorista(Base):
    __tablename__ = "motoristas"
    id_motorista = Column(Integer, primary_key=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    cpf = Column(CHAR(11), unique=True, nullable=False)
    telefone = Column(String(11))
    data_de_nascimento = Column(Date)

class Onibus(Base):
    __tablename__ = "onibus"
    id_onibus = Column(Integer, primary_key=True, index=True)
    placa = Column(VARCHAR(10), unique=True, nullable=False)
    modelo = Column(VARCHAR(50))
    capacidade = Column(Integer, nullable=False)
    turno = Column(VARCHAR(10), nullable=False)
    ar_condicionado = Column(Boolean, default=False)
    banheiro = Column(Boolean, default=False)
    persiana = Column(Boolean, default=False)
    luz_de_leitura = Column(Boolean, default=False)
    tomada = Column(Boolean, default=False)
    id_motorista = Column(Integer, ForeignKey("motoristas.id_motorista"),
    nullable=True)
    id_rota = Column(Integer, ForeignKey("rotas.id_rota"), nullable=True)
    motorista = relationship("Motorista", back_populates="onibus")
    rota = relationship("Rota", back_populates="onibus")    

class Rota(Base):
    __tablename__ = "rotas"
    id_rota = Column(Integer, primary_key=True, index=True)
    nome = Column(VARCHAR(100))
    pontos = Column(Text)
    quantidade_total = Column(Integer)
    quantidade_diaria = Column(Integer)
    onibus = relationship("Onibus", back_populates="rota")
    alunos = relationship("Motorista", secondary="alunos_rotas",
    back_populates="rotas")
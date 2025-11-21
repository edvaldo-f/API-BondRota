from pydantic import BaseModel
from datetime import date
from typing import Optional, List

#Schemas ALuno
class AlunoBase(BaseModel):
    nome: str
    instituicao_de_ensino: Optional[str] = None
    curso: Optional[str] = None
    data_de_nascimento: Optional[date] = None
    cpf: str
    turno: str
    id_rota: Optional[int] = None

class AlunoCreate(AlunoBase):
    pass

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    instituicao_de_ensino: Optional[str] = None
    curso: Optional[str] = None
    data_de_nascimento: Optional[date] = None
    cpf: Optional[str] = None
    turno: Optional[str] = None
    id_rota: Optional[int] = None

class AlunoResponse(AlunoBase):
    id_aluno: int
    class Config:
        from_attributes = True

#Schemas Motorista
class MotoristaBase(BaseModel):
    nome: str
    cpf: str
    telefone: Optional[str] = None
    data_de_nascimento: Optional[date] = None
class MotoristaCreate(MotoristaBase):
    pass
class MotoristaUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    data_de_nascimento: Optional[date] = None
class MotoristaResponse(MotoristaBase):
    id_motorista: int
    class Config:
        from_attributes = True

#Schemas Onibus
class OnibusBase(BaseModel):
    placa: str
    modelo: Optional[str] = None
    capacidade: int
    turno: str
    ar_condicionado: bool = False
    banheiro: bool = False
    persiana: bool = False
    luz_de_leitura: bool = False
    tomada: bool = False
    id_motorista: Optional[int] = None
    id_rota: Optional[int] = None
class OnibusCreate(OnibusBase):
    pass
class OnibusUpdate(BaseModel):
    placa: Optional[str] = None
    modelo: Optional[str] = None
    capacidade: Optional[int] = None
    turno: Optional[str] = None
    ar_condicionado: Optional[bool] = None
    banheiro: Optional[bool] = None
    persiana: Optional[bool] = None
    luz_de_leitura: Optional[bool] = None
    tomada: Optional[bool] = None
    id_motorista: Optional[int] = None
    id_rota: Optional[int] = None
class OnibusResponse(OnibusBase):
    id_onibus: int
    class Config:
        from_attributes = True

#Schemas Rota
class RotaBase(BaseModel):
    nome: str
    pontos: List[str] = None
    quantidade_total: Optional[int] = None
    quantidade_diaria: Optional[int] = None
class RotaCreate(RotaBase):
    pass
class RotaUpdate(BaseModel):
    nome: Optional[str] = None
    pontos: Optional[str] = None
    quantidade_total: Optional[int] = None
    quantidade_diaria: Optional[int] = None
class RotaResponse(RotaBase):
    id_rota: int
    class Config:
        from_attributes = True

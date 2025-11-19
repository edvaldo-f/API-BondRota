from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import alunos, motoristas, onibus, rotas

'''
API com métodos: GET (geral e individual), POST, UPDATE e DELETE
'''
app = FastAPI(tittle="API BondRota.", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alunos.router)
app.include_router(motoristas.router)
app.include_router(onibus.router)
app.include_router(rotas.router)

@app.get("/")
def root():
    return {"message": "API para BondRota - Bem-vindo!"}
@app.get("/health")

def health_check():
    return {"status": "OK"}
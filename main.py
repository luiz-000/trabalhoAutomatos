from fastapi import FastAPI
from endPoints import DFA_EndPoint , DPDA_EndPoint , DTM_EndPoint, NFA_EndPoint


app = FastAPI()


# Registrar os roteadores
app.include_router(DFA_EndPoint.router, prefix='/automata', tags=['DFA'])
app.include_router(DPDA_EndPoint.router, prefix='/automata', tags=['DPDA'])
app.include_router(DTM_EndPoint.router, prefix='/automata', tags=['DTM'])
app.include_router(NFA_EndPoint.router, prefix='/automata', tags=['NFA'])


@app.get("/")
def read_root():
    return {"message": "Trabalho Teoria da Computação"}

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from automata.fa.nfa import NFA
from datetime import datetime
import os

import json

router = APIRouter()



# Modelo para receber dados do Autômato Finito não Determinístico
class NFA_Model(BaseModel):
    states: set[str]
    input_symbols: set[str]
    transitions: dict[str, dict[str, list[str]]]
    initial_state: str
    final_states: set[str]



@router.post('/nfa/create')
def createNFA(nfa_model: NFA_Model):
    
    # Cria e armazena um NFA a partir dos dados fornecidos
    try:
        nfa = NFA(
            states = nfa_model.states,
            input_symbols = nfa_model.input_symbols,
            transitions = nfa_model.transitions,
            initial_state = nfa_model.initial_state,
            final_states = nfa_model.final_states
        )
        
        # Armazenar o NFA em JSON
        with open('automatos/NFA.json', 'w') as f:
            json.dump({
                "states": list(nfa_model.states),
                "input_symbols": list(nfa_model.input_symbols),
                "transitions": nfa_model.transitions,
                "initial_state": nfa_model.initial_state,
                "final_states": list(nfa_model.final_states)
            }, f)
        return {'message': 'NFA criado'}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post('/nfa/test')
def testNFA(entrada: str):
    
    # Testa uma string no NFA armazenado
    try:
        with open('automatos/NFA.json', 'r') as f:
            NFA_Data = json.load(f)
        
        # Recria o objeto NFA a partir dos dados armazenados
        nfa = NFA(
            states = set(NFA_Data["states"]),
            input_symbols = set(NFA_Data["input_symbols"]),
            transitions = NFA_Data["transitions"],
            initial_state = NFA_Data["initial_state"],
            final_states = set(NFA_Data["final_states"]),
        )

        resultado = nfa.accepts_input(entrada)
        return {'Entrada': entrada, 'accepted': resultado}

    except Exception as e:
        raise HTTPException(status_code=400, detail=(e))



@router.get('/nfa/info')
def getInfoNFA():

    # Recupera informações do NFA armazenado
    try:
        with open('automatos/NFA.json', 'r') as f:
            NFA_Data = json.load(f)
        
        return NFA_Data
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Não foi encontrado nenhum NFA')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get('/nfa/grafico')
def getGraficoNFA():

    # Gera o gráfico do NFA armazenado
    try:
        with open('automatos/NFA.json', 'r') as f:
            NFA_Data = json.load(f)

        # Recria o objeto NFA a partir dos dados armazenados
        nfa = NFA(
            states = set(NFA_Data["states"]),
            input_symbols = set(NFA_Data["input_symbols"]),
            transitions = NFA_Data["transitions"],
            initial_state = NFA_Data["initial_state"],
            final_states = set(NFA_Data["final_states"]),
        )
        
        # Criar diretório se não existir
        os.makedirs('graficos_automatos', exist_ok=True)
        if not os.path.exists('graficos_automatos'):
            raise HTTPException(status_code=500, detail='Falha ao criar diretório para gráficos')

        horaSalva = datetime.now().strftime("%Y%m%d_%H%M%S")
        nomeArquivo = f"graficos_automatos/NFA_{horaSalva}.png"

        nfa.show_diagram(path=nomeArquivo)

        if not os.path.exists(nomeArquivo):
            raise HTTPException(status_code=500, detail='Falha ao gerar gráfico')
        
        return FileResponse(nomeArquivo, media_type="image/png")
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Não foi encontrado nenhum NFA para criar um gráfico')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from automata.fa.dfa import DFA
from datetime import datetime
import os

import json

router = APIRouter()



# Modelo para receber dados do Autômato Finito Determinístico
class DFA_Model(BaseModel):
    states: set[str]
    input_symbols: set[str]
    transitions: dict[str, dict[str, str]]
    initial_state: str
    final_states: set[str]



@router.post('/dfa/create')
def createDFA(dfa_model: DFA_Model):
    
    # Cria e armazena um DFA a partir dos dados fornecidos
    try:
        dfa = DFA(
            states = dfa_model.states,
            input_symbols = dfa_model.input_symbols,
            transitions = dfa_model.transitions,
            initial_state = dfa_model.initial_state,
            final_states = dfa_model.final_states
        )
        
        # Armazenar o DFA em JSON
        with open('automatos/DFA.json', 'w') as f:
            json.dump({
                "states": list(dfa_model.states),
                "input_symbols": list(dfa_model.input_symbols),
                "transitions": dfa_model.transitions,
                "initial_state": dfa_model.initial_state,
                "final_states": list(dfa_model.final_states)
            }, f)
        return {'message': 'DFA criado'}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post('/dfa/test')
def testDFA(entrada: str):
    
    # Testa uma string no DFA armazenado
    try:
        with open('automatos/DFA.json', 'r') as f:
            DFA_Data = json.load(f)
        
        # Recria o objeto DFA a partir dos dados armazenados
        dfa = DFA(
            states = set(DFA_Data["states"]),
            input_symbols = set(DFA_Data["input_symbols"]),
            transitions = DFA_Data["transitions"],
            initial_state = DFA_Data["initial_state"],
            final_states = set(DFA_Data["final_states"]),
        )

        resultado = dfa.accepts_input(entrada)
        return {'Entrada': entrada, 'accepted': resultado}

    except Exception as e:
        raise HTTPException(status_code=400, detail=(e))



@router.get('/dfa/info')
def getInfoDFA():

    # Recupera informações do DFA armazenado
    try:
        with open('automatos/DFA.json', 'r') as f:
            DFA_Data = json.load(f)
        
        return DFA_Data
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Não foi encontrado nenhum DFA')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get('/dfa/grafico')
def getGraficoDFA():

    # Gera o gráfico do DFA armazenado
    try:
        with open('automatos/DFA.json', 'r') as f:
            DFA_Data = json.load(f)

        # Recria o objeto DFA a partir dos dados armazenados
        dfa = DFA(
            states = set(DFA_Data["states"]),
            input_symbols = set(DFA_Data["input_symbols"]),
            transitions = DFA_Data["transitions"],
            initial_state = DFA_Data["initial_state"],
            final_states = set(DFA_Data["final_states"]),
        )
        
        # Criar diretório se não existir
        os.makedirs('graficos_automatos', exist_ok=True)
        if not os.path.exists('graficos_automatos'):
            raise HTTPException(status_code=500, detail='Falha ao criar diretório para gráficos')

        horaSalva = datetime.now().strftime("%Y%m%d_%H%M%S")
        nomeArquivo = f"graficos_automatos/DFA_{horaSalva}.png"

        dfa.show_diagram(path=nomeArquivo)

        if not os.path.exists(nomeArquivo):
            raise HTTPException(status_code=500, detail='Falha ao gerar gráfico')
        
        return FileResponse(nomeArquivo, media_type="image/png")
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Não foi encontrado nenhum DFA para criar um gráfico')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

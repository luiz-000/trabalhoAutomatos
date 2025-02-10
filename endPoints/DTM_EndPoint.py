from fastapi import APIRouter , HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from automata.tm.dtm import DTM
from graphviz import Digraph
from datetime import datetime
import os

import json

router = APIRouter()



# Modelo para receber dados da Máquina de Turing Determinística
class DTM_Model(BaseModel):
    states: set[str]
    input_symbols: set[str]
    tape_symbols: set[str]
    transitions: dict[str, dict[str, tuple[str, str, str]]]
    initial_state: str
    blank_symbol: str
    final_states: set[str]



@router.post('/dtm/create')
def createDTM(dtm_model: DTM_Model):

    # Cria e armazena uma DTM a partir dos dados fornecidos
    try:
        dtm = DTM(
            states = dtm_model.states,
            input_symbols = dtm_model.input_symbols,
            tape_symbols = dtm_model.tape_symbols,
            transitions = dtm_model.transitions,
            initial_state = dtm_model.initial_state,
            blank_symbol = dtm_model.blank_symbol,
            final_states = dtm_model.final_states
        )

        # Armazenar a DTM em JSON
        with open('automatos/DTM.json', 'w') as f:
            json.dump({
                "states": list(dtm_model.states),
                "input_symbols": list(dtm_model.input_symbols),
                "tape_symbols": list(dtm_model.tape_symbols),
                "transitions": dtm_model.transitions,
                "initial_state": dtm_model.initial_state,
                "blank_symbol": dtm_model.blank_symbol,
                "final_states": list(dtm_model.final_states)
            }, f)
        return {'message': 'DTM criada'}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post('/dtm/test')
def testDTM(entrada: str):

    # Testa uma string na DTM armazenada
    try:
        with open('automatos/DTM.json', 'r') as f:
            DTM_Data = json.load(f)
        
        # Recria o objeto DTM a partir dos dados armazenados
        dtm = DTM(
            states = set(DTM_Data["states"]),
            input_symbols = set(DTM_Data["input_symbols"]),
            tape_symbols = set(DTM_Data["tape_symbols"]),
            transitions = DTM_Data["transitions"],
            initial_state = DTM_Data["initial_state"],
            blank_symbol = DTM_Data["blank_symbol"],
            final_states = set(DTM_Data["final_states"]),
        )

        resultado = dtm.accepts_input(entrada)
        return {'Entrada': entrada, 'accepted': resultado}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get('/dtm/info')
def getInfoDTM():

    # Recupera informações da DTM armazenada
    try:
        with open('automatos/DTM.json', 'r') as f:
            DTM_Data = json.load(f)

        return DTM_Data
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Não foi encontrado nenhuma DTM')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get('/dtm/grafico')
def getGraficoDTM():

    # Gera o gráfico da DTM armazenada
    try:
        with open('automatos/DTM.json', 'r') as f:
            DTM_Data = json.load(f)
        
        # Recria o objeto DTM a partir dos dados armazenados
        dtm = DTM(
            states = set(DTM_Data["states"]),
            input_symbols = set(DTM_Data["input_symbols"]),
            tape_symbols = set(DTM_Data["tape_symbols"]),
            transitions = DTM_Data["transitions"],
            initial_state = DTM_Data["initial_state"],
            blank_symbol = DTM_Data["blank_symbol"],
            final_states = set(DTM_Data["final_states"]),
        )

        dot = Digraph()
        dot.attr(rankdir='LR')
        
        # Adiciona estados
        for state in dtm.states:
            if state in dtm.final_states:
                dot.node(str(state), str(state), shape='doublecircle')
            elif state == dtm.initial_state:
                dot.node(str(state), str(state), shape='circle', style='bold')
            else:
                dot.node(str(state), str(state), shape='circle')
        
        # Adiciona transições
        for current_state, transitions in dtm.transitions.items():
            for symbol, transition in transitions.items():
                next_state, write_symbol, direction = transition
                label = f"{symbol} → {write_symbol}, {direction}"
                dot.edge(str(current_state), str(next_state), label=label)
        
        # Criar diretório se não existir
        os.makedirs('graficos_automatos', exist_ok=True)
        if not os.path.exists('graficos_automatos'):
            raise HTTPException(status_code=500, detail='Falha ao criar diretório para gráficos')
        
        horaSalva = datetime.now().strftime("%Y%m%d_%H%M%S")
        nomeArquivo = f"graficos_automatos/DTM_{horaSalva}"

        dot.render(nomeArquivo, format='png', cleanup=True)

        return FileResponse(f"{nomeArquivo}.png", media_type="image/png")
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Não foi encontrado nenhuma DTM para criar um gráfico')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

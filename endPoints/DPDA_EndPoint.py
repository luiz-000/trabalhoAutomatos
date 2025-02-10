from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from automata.pda.dpda import DPDA
from datetime import datetime
import os

import json

router = APIRouter()



# Modelo para receber dados do Autômato de Pilha Determinístico
class DPDA_Model(BaseModel):
    states: set[str]
    input_symbols: set[str]
    stack_symbols: set[str]
    transitions: dict[str, dict[str, dict[str, tuple[str, list[str]]]]]
    initial_state: str
    initial_stack_symbol: str
    final_states: set[str]
    acceptance_mode: str



@router.post('/dpda/create')
def createDPDA(dpda_model: DPDA_Model):

    # Cria e armazena um DPDA a partir dos dados fornecidos
    try:
        dpda = DPDA(
            states = dpda_model.states,
            input_symbols = dpda_model.input_symbols,
            stack_symbols = dpda_model.stack_symbols,
            transitions = dpda_model.transitions,
            initial_state = dpda_model.initial_state,
            initial_stack_symbol = dpda_model.initial_stack_symbol,
            final_states = dpda_model.final_states,
            acceptance_mode = dpda_model.acceptance_mode
        )

        # Armazenar o DPDA em JSON
        with open('automatos/DPDA.json', 'w') as f:
            json.dump({
                "states": list(dpda_model.states),
                "input_symbols": list(dpda_model.input_symbols),
                "stack_symbols": list(dpda_model.stack_symbols),
                "transitions": dpda_model.transitions,
                "initial_state": dpda_model.initial_state,
                "initial_stack_symbol": dpda_model.initial_stack_symbol,
                "final_states": list(dpda_model.final_states),
                "acceptance_mode": dpda_model.acceptance_mode
            }, f)
        return {'message': 'DPDA criado'}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post('/dpda/test')
def testeDPDA(entrada: str):

    # Testa uma string no DPDA armazenado
    try:
        with open('automatos/DPDA.json', 'r') as f:
            DPDA_Data = json.load(f)

        # Recria o objeto DPDA a partir dos dados armazenados
        dpda = DPDA(
            states = set(DPDA_Data["states"]),
            input_symbols = set(DPDA_Data["input_symbols"]),
            stack_symbols = set(DPDA_Data["stack_symbols"]),
            transitions = DPDA_Data["transitions"],
            initial_state = DPDA_Data["initial_state"],
            initial_stack_symbol = DPDA_Data["initial_stack_symbol"],
            final_states = set(DPDA_Data["final_states"]),
            acceptance_mode = DPDA_Data["acceptance_mode"],
        )

        resultado = dpda.accepts_input(entrada)
        return {'Entrada': entrada, 'accepted': resultado}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=(e))



@router.get('/dpda/info')
def getInfoDPDA():

    # Recupera informações do DPDA armazenado
    try:
        with open('automatos/DPDA.json', 'r') as f:
            DPDA_Data = json.load(f)

        return DPDA_Data
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Não foi encontrado nenhum DPDA')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get('/dpda/grafico')
def getGraficoDPDA():

    # Gera o gráfico do DPDA armazenado
    try:
        with open('automatos/DPDA.json', 'r') as f:
            DPDA_Data = json.load(f)

        # Recria o objeto DPDA a partir dos dados armazenados
        dpda = DPDA(
            states = set(DPDA_Data["states"]),
            input_symbols = set(DPDA_Data["input_symbols"]),
            stack_symbols = set(DPDA_Data["stack_symbols"]),
            transitions = DPDA_Data["transitions"],
            initial_state = DPDA_Data["initial_state"],
            initial_stack_symbol = DPDA_Data["initial_stack_symbol"],
            final_states = set(DPDA_Data["final_states"]),
            acceptance_mode = DPDA_Data["acceptance_mode"],
        )

        # Criar diretório se não existir
        os.makedirs('graficos_automatos', exist_ok=True)
        if not os.path.exists('graficos_automatos'):
            raise HTTPException(status_code=500, detail='Falha ao criar diretório para gráficos')

        horaSalva = datetime.now().strftime("%Y%m%d_%H%M%S")
        nomeArquivo = f"graficos_automatos/DPDA_{horaSalva}.png"

        dpda.show_diagram(path=nomeArquivo)
        
        if not os.path.exists(nomeArquivo):
            raise HTTPException(status_code=500, detail='Falha ao gerar gráfico')

        return FileResponse(nomeArquivo, media_type="image/png")
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='Não foi encontrado nenhum DPDA para criar um gráfico')
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

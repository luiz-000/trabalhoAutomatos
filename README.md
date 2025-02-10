# PROJETO DE AUTÔMATOS COM FASTAPI:

Este projeto permite a criação, manipulação e análise de diferentes tipos de autômatos, incluindo Autômatos Finitos Não Determinísticos (NFA),
Autômatos Finitos Determinísticos (DFA), Máquinas de Turing Determinísticas (DTM) e Autômatos de Pilha Determinísticos (DPDA).

Foi criado utilizando Python juntamente com FastApi e a biblioteca Automata-lib.

O projeto foi desenvolvido como trabalho final da disciplina Teoria da Computação.

<br>

## TECNOLOGIAS UTILIZADAS:
* Python 3.12  
* Conda  


### BIBLIOTECAS:
* FastAPI  
* Uvicorn  
* Pydantic  
* Automata-lib  
* Graphviz  
* PyGraphviz

<br>

## CONFIGURAÇÃO DO AMBIENTE:

### Instalação do Conda:  
1- Baixe e instale o Miniconda ou Anaconda.

2- Crie um ambiente virtual:

```
conda create -n automata_env python=3.12

conda activate automata_env
```

<br>

## INSTAÇÃO DAS DEPENDÊNCIAS:

```
conda install -c conda-forge graphviz pygraphviz

conda install pydantic -c conda-forge

pip install fastapi uvicorn automata-lib
```

<br>

## COMO USAR:

### Iniciar a API:

```
uvicorn app.main:app --reload
```


### Testar no Navegador
Acesse a interface interativa da API via: http://127.0.0.1:8000/docs

<br>

## ESTRUTURA DO PROJETO:
```
trabalhoTeoria/
├── automatos/
│   └── DFA.json
│   └── DPDA.json
│   └── DTM.json
│   └── NFA.json
|
├── endPoints/
│   └── DFA_EndPoint.py
│   └── DPDA_EndPoint.py
│   └── DTM_EndPoint.py
│   └── NFA_EndPoint.py
|
├── exemplos_automatos/
│   └── DFA.txt
│   └── DPDA.txt
│   └── DTM.txt
│   └── NFA.txt
|
├── README.md
├── main.py
```

<br>

## Funcionalidades

* Criação de diferentes tipos de autômatos.
* Salvamento de autômatos em arquivo JSON.
* Verificação de aceitação de entradas.
* Recuperação de informações sobre o autômato salvo.
* Geração de diagramas de autômatos.

<br>

## API Endpoints

### Criar Autômato:

#### POST /automata/create
* Corpo da Requisição: JSON com definição do autômato.
* Resposta: Mensagem de Sucesso.


### Verificar Entrada:

#### POST /automata/test
* Corpo da Requisição: String de entrada.
* Resposta: Booleano indicando aceitação ou negação.


### Obter Informações do Autômato:

#### GET /automata/info

* Resposta: Detalhes completos do autômato.


### Gerar Gráfico do Autômato:

#### GET /automata/grafico

* Resposta: Arquivo de imagem do respectivo autômato.

<br>

## Exemplo de Uso

### Criação de um DFA:

```
{
    "states": ["q0", "q1", "q2"],
    "input_symbols": ["0", "1"],
    "transitions": {
        "q0": {
            "0": "q0",
            "1": "q1"
        },
        "q1": {
            "0": "q0",
            "1": "q2"
        },
        "q2": {
            "0": "q2",
            "1": "q1"
        }
    },
    "initial_state": "q0",
    "final_states": ["q1"]
}
```

### Teste de Entrada:

```
000111
```

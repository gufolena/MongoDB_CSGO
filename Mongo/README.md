# CS:GO Player Analysis with MongoDB

Este projeto utiliza MongoDB para realizar análises detalhadas de jogadores de CS:GO (Counter-Strike: Global Offensive). Ele realiza várias consultas simples e avançadas para explorar dados sobre jogadores, incluindo seus kills, desempenho em mapas, assistências, relações de kills por round, entre outras métricas.

Link do arquivo csv: https://www.kaggle.com/datasets/naumanaarif/csgo-pro-players-dataset

## Índice

1. [Requisitos](#requisitos)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Consultas Simples](#consultas-simples)
5. [Consultas Avançadas](#consultas-avançadas)
6. [Execução das Consultas](#execução-das-consultas)
7. [Estrutura do Projeto](#estrutura-do-projeto)
8. [Contribuição](#contribuição)
9. [Licença](#licença)

## Requisitos

- Python 3.x
- MongoDB
- PyMongo (biblioteca Python para conectar e interagir com MongoDB)
- Pandas
- Dash
- Plotly
- Streamlit

## Instalação

1. Instale o MongoDB seguindo as instruções do [site oficial](https://www.mongodb.com/try/download/community).

2. Instale as dependências do projeto, como o PyMongo, executando:
   ```bash
   pip install pymongo
   ```

## Configuração

1. Certifique-se de que o servidor MongoDB esteja em execução localmente:
   ```bash
   mongod
   ```

2. Configure a conexão com o MongoDB em seu código:
   ```python
   from pymongo import MongoClient

   client = MongoClient("mongodb://localhost:27017/")
   db = client['csgo_db']
   players_collection = db['players']
   ```

3. Adicione os dados dos jogadores à sua coleção MongoDB (`players_collection`) se ainda não o fez.

## Consultas Simples

O projeto inclui várias consultas simples para obter insights básicos sobre os jogadores:

1. **Porcentagem de mapas com mais de X kills**:
   - Calcula a porcentagem de mapas nos quais um jogador obteve mais de X kills.

2. **Ranking de jogadores com base na relação kills/round e assistências/round**:
   - Classifica jogadores com base na combinação de kills e assistências por round.

3. **Diferença de kills entre jogadores com mais de X mapas jogados**:
   - Calcula a diferença entre o jogador com mais kills e o jogador com menos kills, considerando aqueles que jogaram mais de X mapas.

4. **Jogadores com mais de X opening kills e rating acima de Y**:
   - Filtra jogadores que possuem um número elevado de opening kills e um rating acima de um limite definido.

5. **Top killers em cada categoria de arma**:
   - Identifica o jogador com mais kills para cada categoria de arma.

## Consultas Avançadas

Consultas mais complexas que oferecem análises detalhadas:

1. **Percentual de vitórias após o primeiro kill por país**:
   - Calcula a média de vitórias das equipes de cada país após o primeiro kill, filtrando por países com percentuais altos.

2. **Média de kills por país para jogadores com mais de X mapas jogados**:
   - Determina a média de kills por país considerando jogadores com alta experiência.

3. **Distribuição de kill/death ratio por faixa etária**:
   - Analisa a distribuição do K/D ratio dos jogadores, agrupados por faixas etárias.

4. **Ranking de kills por round com baixa taxa de headshot**:
   - Classifica jogadores com alta taxa de kills por round, mas com uma taxa de headshot abaixo de um determinado limite.

5. **Total de kills por tipo de arma por time**:
   - Resume o total de kills por cada tipo de arma, agrupado por time.

6. **Diferença de kills/deaths para jogadores com mais de X mapas e Y kills**:
   - Calcula a diferença entre kills e deaths para jogadores altamente experientes.

## Execução das Consultas

Para executar as consultas, basta chamar as funções definidas no código Python. Exemplo:

```python
# Exemplo de consulta para verificar a porcentagem de mapas com mais de 1000 kills para um jogador específico
percentage_kills = percentage_maps_with_kills_above(11893, 1000)
print(f"Porcentagem de mapas com mais de 1000 kills: {percentage_kills}%")
```

Cada consulta retorna uma lista de resultados que pode ser facilmente iterada para exibir as informações desejadas.

## Estrutura do Projeto

- `csgo_analysis.py`: Arquivo principal contendo todas as funções de consulta.
- `README.md`: Documentação do projeto.
- `requirements.txt`: Lista de dependências do projeto.

## Contribuição

Contribuições são bem-vindas! Se você encontrar um bug ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma _issue_ ou enviar um _pull request_.

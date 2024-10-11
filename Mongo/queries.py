from pymongo import MongoClient


# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['csgo_db']
players_collection = db['players']

# ======================
# Consultas Simples
# ======================

# 1. Porcentagem de mapas com mais de X kills
def percentage_maps_with_kills_above(player_id, kill_threshold):
    player = players_collection.find_one({"player_id": player_id})
    maps_with_kills_above = player['maps_played'] - player['0_kill_rounds']
    percentage = (maps_with_kills_above / player['maps_played']) * 100
    return percentage

# 2. Ranking dos jogadores com base na relação de kills por round e assistências por round
def ranking_kills_assists():
    pipeline = [
        {
            "$project": {
                "nickname": 1,
                "kills_per_round": 1,
                "assists_per_round": 1,
                "total_kills": 1,
                "total_assists": 1,
                "total_rounds": "$rounds_played",  # Apenas para referência
                "kills_assists_ratio": {
                    "$add": ["$kills_per_round", "$assists_per_round"]
                }
            }
        },
        {
            "$sort": {
                "kills_assists_ratio": -1  # Ordenar do maior para o menor
            }
        },
        {
            "$limit": 10  # Top 10 jogadores
        }
    ]
    
    result = players_collection.aggregate(pipeline)
    return list(result)

# 3. Diferença de kills entre jogadores com mais de X mapas jogados
def kill_difference_among_players_with_maps_above(threshold):
    result = players_collection.aggregate([
        {"$match": {"maps_played": {"$gt": threshold}}},
        {"$group": {
            "_id": None,
            "max_kills": {"$max": "$total_kills"},
            "min_kills": {"$min": "$total_kills"}
        }},
        {"$project": {"kill_difference": {"$subtract": ["$max_kills", "$min_kills"]}}}
    ])
    return list(result)

# 4. Jogadores com mais de X opening kills e rating acima de Y
def players_with_opening_kills_and_rating_above(opening_kills_threshold, rating_threshold):
    result = players_collection.find({
        "total_opening_kills": {"$gt": opening_kills_threshold},
        "rating": {"$gt": rating_threshold}
    })
    return list(result)

# 5. Função para encontrar o jogador com mais kills em cada categoria
def get_top_killers():
    categories = ['rifle_kills', 'sniper_kills', 'smg_kills', 'pistol_kills', 'grenade_kills']
    results = {}
    
    for category in categories:
        top_killer = players_collection.find_one({}, sort=[(category, -1)], projection={'player_id': 1, 'nickname': 1, category: 1})
        results[category] = top_killer
    
    return results

# ======================
# Consultas Avançadas
# ======================

# 6. Jogadores com mais de X% de vitórias após o primeiro kill
def players_with_win_percent_after_first_kill_above(threshold):
    result = players_collection.find({"team_win_percent_after_first_kill": {"$gt": threshold}})
    return list(result)


# 7. Calcula a porcentagem média de vitórias das equipes após o primeiro kill, filtrando apenas os países com uma porcentagem superior a um limite definido, e ordena os resultados pela média de vitórias em ordem decrescente.
def win_percentage_after_first_kill_by_country(threshold):
    pipeline = [
        {
            "$addFields": {
                # Remover o símbolo de '%' e converter para número
                "team_win_percent_after_first_kill_num": {
                    "$convert": {
                        "input": {"$substr": ["$team_win_percent_after_first_kill", 0, -1]},  # Remove o '%'
                        "to": "double",
                        "onError": 0  # Valor de fallback em caso de erro na conversão
                    }
                }
            }
        },
        {"$match": {"team_win_percent_after_first_kill_num": {"$gt": threshold}}},
        {"$group": {
            "_id": "$country",
            "average_win_percent": {"$avg": "$team_win_percent_after_first_kill_num"},
            "total_players": {"$sum": 1}
        }},
        {"$sort": {"average_win_percent": -1}}
    ]
    result = players_collection.aggregate(pipeline)
    return list(result)

# 8. Média de kills por país para jogadores com mais de X mapas jogados
def average_kills_by_country(min_maps_played):
    pipeline = [
        {"$match": {"maps_played": {"$gt": min_maps_played}}},
        {"$group": {
            "_id": "$country",
            "average_kills": {"$avg": "$total_kills"},
            "total_players": {"$sum": 1}
        }},
        {"$sort": {"average_kills": -1}}
    ]
    result = players_collection.aggregate(pipeline)
    return list(result)

# 9. Distribuição de kill/death ratio por faixa etária
def kd_ratio_by_age_group():
    pipeline = [
        {"$bucket": {
            "groupBy": "$age",
            "boundaries": [18, 21, 25, 30, 35, 40],  # Definindo os grupos etários
            "default": "Other",
            "output": {
                "average_kd_ratio": {"$avg": "$kills_per_death"},
                "total_players": {"$sum": 1}
            }
        }},
        {"$sort": {"average_kd_ratio": -1}}
    ]
    result = players_collection.aggregate(pipeline)
    return list(result)

# 10. Ranking dos jogadores com maior número de kills por round (headshot < 40%)
def top_kill_per_round_low_headshot(threshold):
    pipeline = [
        {
            "$addFields": {
                "headshot_percentage_num": {
                    "$convert": {
                        "input": {"$substr": ["$headshot_percentage", 0, -1]},
                        "to": "double",
                        "onError": 0
                    }
                }
            }
        },
        {
            "$match": {
                "headshot_percentage_num": {"$lt": threshold}
            }
        },
        {
            "$sort": {"kills_per_round": -1}
        },
        {
            "$project": {
                "nickname": 1,
                "kills_per_round": 1,
                "headshot_percentage": 1
            }
        },
        {
            "$limit": 10
        }
    ]
    result = players_collection.aggregate(pipeline)
    return list(result)




# 11. Total de kills por tipo de arma por time
def total_kills_by_weapon_per_team():
    pipeline = [
        {"$group": {
            "_id": "$current_team",
            "rifle_kills": {"$sum": "$rifle_kills"},
            "sniper_kills": {"$sum": "$sniper_kills"},
            "smg_kills": {"$sum": "$smg_kills"},
            "pistol_kills": {"$sum": "$pistol_kills"},
            "grenade_kills": {"$sum": "$grenade_kills"},
            "other_kills": {"$sum": "$other_kills"}
        }},
        {"$sort": {"rifle_kills": -1}}
    ]
    result = players_collection.aggregate(pipeline)
    return list(result)

# 12. Diferença de kills/deaths para jogadores com mais de X mapas jogados e mais de Y kills
def kill_death_difference_by_maps_and_kills(min_maps_played, min_kills):
    pipeline = [
        {"$match": {
            "maps_played": {"$gt": min_maps_played},
            "total_kills": {"$gt": min_kills}
        }},
        {"$project": {
            "nickname": 1,
            "kill_to_death_diff": {"$subtract": ["$total_kills", "$total_deaths"]}
        }},
        {"$sort": {"kill_to_death_diff": -1}},
        {"$limit": 10}
    ]
    result = players_collection.aggregate(pipeline)
    return list(result)

# ======================
# Execução de Consultas Simples
# ======================

print("\n===== Consultas Simples =====")

# 1. Porcentagem de mapas com mais de 1000 kills para o jogador com ID 11893
print("\nPorcentagem de mapas com mais de 1000 kills")
percentage_kills = percentage_maps_with_kills_above(11893, 1000)
print(f"Jogador ID: 11893 - Porcentagem de mapas com mais de 1000 kills: {percentage_kills}%")

# 2. Ranking dos jogadores com base na relação de kills por round e assistências por round
print("\nRanking dos jogadores com base na relação de kills e assistências por round:")
ranking_results = ranking_kills_assists()
for idx, result in enumerate(ranking_results, start=1):
    print(f"{idx}. Nickname: {result['nickname']} - Kills/Round: {result['kills_per_round']} - Assists/Round: {result['assists_per_round']} - Kills/Assists Ratio: {result['kills_assists_ratio']:.2f}")

# 3. Diferença de kills entre jogadores com mais de 500 mapas jogados
print("\nDiferença de kills entre jogadores com mais de 500 mapas jogados")
kill_diff_results = kill_difference_among_players_with_maps_above(500)
for result in kill_diff_results:
    print(f"Diferença de kills: {result['kill_difference']}")

# 4. Jogadores com mais de 1000 opening kills e rating acima de 1.1
print("\nJogadores com mais de 1000 opening kills e rating acima de 1.1")
opening_kill_rating_results = players_with_opening_kills_and_rating_above(1000, 1.1)
for result in opening_kill_rating_results:
    print(f"Nickname: {result['nickname']} - Opening Kills: {result['total_opening_kills']} - Rating: {result['rating']}")

# 5. Jogador com mais kills em cada categoria
print("\nJogador com mais kills em cada categoria")
top_killers = get_top_killers()
for category, player in top_killers.items():
    print(f"Top player for {category}: {player['nickname']} with {player[category]} kills")

# ======================
# Execução de Consultas Avançadas
# ======================

print("\n===== Consultas Avançadas =====")

# 1. Porcentagem de vitórias após o primeiro kill acima de 40% por país
print("\nPorcentagem de vitórias após o primeiro kill acima de 40% por país")
win_percent_results = win_percentage_after_first_kill_by_country(40)
for result in win_percent_results:
    print(f"País: {result['_id']} - Média de vitórias: {result['average_win_percent']}% - Jogadores: {result['total_players']}")

# 2. Média de kills por país para jogadores com mais de 500 mapas jogados
print("\nMédia de kills por país para jogadores com mais de 500 mapas jogados")
avg_kills_results = average_kills_by_country(500)
for result in avg_kills_results:
    print(f"País: {result['_id']} - Média de kills: {result['average_kills']} - Jogadores: {result['total_players']}")

# 3. Distribuição do kill/death ratio por faixa etária
print("\nDistribuição do kill/death ratio por faixa etária")
kd_ratio_results = kd_ratio_by_age_group()
for result in kd_ratio_results:
    print(f"Faixa etária: {result['_id']} - Média de K/D: {result['average_kd_ratio']} - Jogadores: {result['total_players']}")

# 4. Ranking dos jogadores com maior número de kills por round, mas com uma taxa de headshot abaixo de 40%
print("\nRanking dos jogadores com maior número de kills por round (headshot < 40%)")

low_headshot_results = top_kill_per_round_low_headshot(40.0)

for idx, result in enumerate(low_headshot_results, 1):
    print(f"{idx}. Nickname: {result.get('nickname', 'N/A')} - Kills/Round: {result.get('kills_per_round', 'N/A')} - Headshot %: {result.get('headshot_percentage', 'N/A')}")

# 5. Total de kills por tipo de arma por time
print("\nTotal de kills por tipo de arma por time")
kills_by_weapon_results = total_kills_by_weapon_per_team()
for result in kills_by_weapon_results:
    print(f"Time: {result['_id']} - Rifle Kills: {result['rifle_kills']} - Sniper Kills: {result['sniper_kills']} - SMG Kills: {result['smg_kills']}")

# 6. Diferença de kills/deaths para jogadores com mais de 500 mapas jogados e mais de 10,000 kills
print("\nDiferença de kills/deaths para jogadores com mais de 500 mapas jogados e mais de 10,000 kills")
kill_death_diff_results = kill_death_difference_by_maps_and_kills(500, 10000)
for idx, result in enumerate(kill_death_diff_results, 1):
    print(f"{idx}. Nickname: {result['nickname']} - Diferença K/D: {result['kill_to_death_diff']}")

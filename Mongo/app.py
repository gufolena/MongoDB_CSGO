# app.py
import streamlit as st
import plotly.express as px
import queries

# Configurações iniciais da página
st.set_page_config(page_title="CS:GO Player Stats Dashboard", layout="wide")

# Título da aplicação
st.title("📊 Dashboard de Análise de Jogadores de CS:GO")

# Organização do layout usando abas
tab1, tab2, tab3, tab4= st.tabs([
    "🔹 Mapas com Mais de X Kills",
    "🏆 Ranking de Jogadores",
    "⚔️ Diferença de Kills",
    "🔫 Top Kills por Categoria",
])

# Defina as cores para cada categoria
category_colors = {
    'rifle_kills': '#3498db',  # azul
    'sniper_kills': '#9b59b6',  # roxo
    'smg_kills': '#2ecc71',     # verde
    'pistol_kills': '#f1c40f',  # amarelo
    'grenade_kills': '#e74c3c'  # vermelho
}

# Defina os emojis para cada categoria
category_emojis = {
    'rifle_kills': '🔫',            # Pistola (não há emoji específico para rifle)
    'sniper_kills': '🎯',           # Alvo para Sniper
    'smg_kills': '🔫',               # Pistola para SMG
    'pistol_kills': '🔫',            # Pistola
    'grenade_kills': '🧨'            # Granada
}



# ----------------------------
# Aba 1: Porcentagem de Mapas
# ----------------------------
with tab1:
    st.header("1. Porcentagem de Mapas com Mais de X Kills")
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        # Lista de IDs de jogadores (exemplo)
        player_ids = [11893, 7998, 20113, 13156,13779, 2023]  # Insira a lista de IDs reais dos jogadores
        player_id = st.selectbox("🔍 ID do Jogador", player_ids)

    with col2:
        kill_threshold = st.number_input("🔢 Limiar de Kills", value=1000, step=100, min_value=0)

    with col3:
        if st.button("📈 Atualizar"):
            with st.spinner("Calculando..."):
                percentage = queries.percentage_maps_with_kills_above(player_id, kill_threshold)
            if percentage is not None:
                st.success(f"Jogador ID: {player_id} - **{percentage:.2f}%** dos mapas têm mais de {kill_threshold} kills.")
            else:
                st.error("Dados insuficientes para calcular a porcentagem.")

# --------------------------------------------------------
# Aba 2: Ranking de Jogadores (Kills/Assistências por Round)
# --------------------------------------------------------
with tab2:
    st.header("2. Ranking de Jogadores (Kills/Assistências por Round)")
    ranking = queries.ranking_kills_assists()
    if ranking:
        df = {
            'Nickname': [player['nickname'] for player in ranking],
            'Kills + Assistências por Round': [player['kills_assists_ratio'] for player in ranking],
            'Kills por Round': [player['kills_per_round'] for player in ranking],
            'Assistências por Round': [player['assists_per_round'] for player in ranking],
        }
        fig = px.bar(
            x=df['Nickname'],
            y=df['Kills + Assistências por Round'],
            labels={'x': 'Jogadores', 'y': 'Kills + Assistências por Round'},
            title='🏆 Top 10 Jogadores por Relação Kills/Assistências por Round',
            color=df['Kills + Assistências por Round'],
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            xaxis_title='Jogadores',
            yaxis_title='Kills + Assistências por Round',
            title_x=0.5,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Nenhum dado disponível para o ranking.")

# -----------------------------------------------------------------
# Aba 3: Diferença de Kills (Jogadores com mais de X Mapas)
# -----------------------------------------------------------------
with tab3:
    st.header("3. Diferença de Kills (Jogadores com mais de X Mapas)")
    maps_threshold = st.number_input("🔢 Mapas Mínimos", value=500, step=10, min_value=0)
    
    if st.button("⚔️ Calcular Diferença"):
        with st.spinner("Calculando..."):
            result = queries.kill_difference_among_players_with_maps_above(maps_threshold)
        if result:
            kill_diff = result[0].get('kill_difference', 'N/A')
            st.success(f"Diferença de kills entre jogadores com mais de **{maps_threshold}** mapas jogados: **{kill_diff}**.")
        else:
            st.error("Nenhum resultado encontrado.")

# --------------------------------------------------------
# Aba 4: Jogador com Mais Kills por Categoria
# --------------------------------------------------------
with tab4:
    st.header("4. Jogador com Mais Kills por Categoria")
    top_killers = queries.get_top_killers()
    
    if top_killers:
        for category, player in top_killers.items():
            # Obter o nome da categoria e o emoji correspondente
            category_name = category.replace('_', ' ').title()
            emoji = category_emojis.get(category, '🔫')  # Emoji padrão caso não esteja no dicionário
            kills = player.get(category, 0) if player else 0
            
            # Exibir o título com o emoji
            st.markdown(f"### {emoji} {category_name}")
            
            if player:
                st.write(f"**Top Killer:** {player['nickname']} com **{kills}** kills")
                
                # Definir a cor com base na categoria
                color = category_colors.get(category, '#95a5a6')  # Cor padrão cinza
                
                # Criação do gráfico de barras
                fig = px.bar(
                    x=[player['nickname']],
                    y=[kills],
                    labels={'x': 'Jogador', 'y': 'Número de Kills'},
                    title=f"{category_name} - Top Killer",
                    color_discrete_sequence=[color]
                )
                fig.update_layout(template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("**Top Killer:** Nenhum dado disponível")
    else:
        st.error("Nenhum dado disponível para os top killers.")



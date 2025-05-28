import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Análise Comercial", layout="wide")
st.title("📊 Análise Comercial com Dados de Vendas")

# Upload do arquivo
uploaded_file = st.file_uploader("📂 Envie a tabela tratada (.xlsx)", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Normalização dos nomes das colunas
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Conversão de datas
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')

    # Menu lateral
    aba = st.sidebar.radio("🔎 Escolha uma Análise:", [
        "1. Produtos mais buscados por perfil ou região",
        "2. Atendimento vs Avaliação",
        "3. Comportamento de Recompra",
        "4. Abandono de Carrinho por Categoria"
    ])

    # 1. Produtos mais buscados por perfil ou região
    if aba == "1. Produtos mais buscados por perfil ou região":
        st.header("🛒 Produtos mais buscados")

        col1, col2 = st.columns(2)

        if 'categoria.1' in df.columns and 'categoria' in df.columns:
            with col1:
                perfil = st.selectbox("Selecione o Perfil do Cliente:", df['categoria.1'].dropna().unique())
                df_perfil = df[df['categoria.1'] == perfil]
                top_perfil = df_perfil['categoria'].value_counts()
                fig = px.bar(top_perfil, title=f"Top categorias de produtos para o perfil: {perfil}")
                st.plotly_chart(fig, use_container_width=True)

        if 'cidade' in df.columns:
            with col2:
                cidade = st.selectbox("Selecione a Cidade (Região):", df['cidade'].dropna().unique())
                df_cidade = df[df['cidade'] == cidade]
                top_cidade = df_cidade['categoria'].value_counts()
                fig = px.bar(top_cidade, title=f"Top categorias de produtos para a cidade: {cidade}")
                st.plotly_chart(fig, use_container_width=True)

    # 2. Atendimento vs Avaliação
    elif aba == "2. Atendimento vs Avaliação":
        st.header("🤝 Atendimento influencia nas avaliações?")

        if 'avaliacao_servico' in df.columns and 'categoria' in df.columns:
            # Filtra avaliações válidas
            avaliacoes_validas = df.dropna(subset=['avaliacao_servico']).copy()

            # Categorização das faixas
            def classificar_avaliacao(nota):
                if nota <= 4:
                    return "Negativa"
                elif nota <= 6:
                    return "Ligeiramente Negativa"
                elif nota <= 8:
                    return "Positiva"
                else:
                    return "Altamente Positiva"

            avaliacoes_validas['faixa_avaliacao'] = avaliacoes_validas['avaliacao_servico'].apply(classificar_avaliacao)

            # Agrupamento por categoria de produto e faixa
            agrupado = avaliacoes_validas.groupby(['categoria', 'faixa_avaliacao'])['id_venda'].count().reset_index()
            agrupado.rename(columns={'id_venda': 'Quantidade'}, inplace=True)

            # Gráfico de barras empilhadas
            fig = px.bar(agrupado,
                         x='categoria',
                         y='Quantidade',
                         color='faixa_avaliacao',
                         title="Distribuição das Avaliações por Categoria",
                         labels={"categoria": "Categoria de Produto", "faixa_avaliacao": "Faixa de Avaliação"},
                         color_discrete_map={
                             "Negativa": "#EF553B",
                             "Ligeiramente Negativa": "#FFA15A",
                             "Positiva": "#00CC96",
                             "Altamente Positiva": "#636EFA"
                         })
            st.plotly_chart(fig, use_container_width=True)

    # 3. Comportamento de Recompra
    elif aba == "3. Comportamento de Recompra":
        st.header("🔁 Recompra dos Clientes")
        if 'id_cliente' in df.columns and 'data_venda' in df.columns:
            df = df.sort_values(by=['id_cliente', 'data_venda'])
            df['dias_para_recompra'] = df.groupby('id_cliente')['data_venda'].diff().dt.days
            fig = px.histogram(df['dias_para_recompra'].dropna(), nbins=30,
                               title="Tempo entre compras por cliente (em dias)",
                               labels={"dias_para_recompra": "Dias para nova compra"})
            st.plotly_chart(fig, use_container_width=True)
            st.metric("⏱️ Tempo médio entre compras", f"{df['dias_para_recompra'].mean():.1f} dias")

    # 4. Abandono de Carrinho por Categoria
    elif aba == "4. Abandono de Carrinho por Categoria":
        st.header("🛒 Padrões de Abandono de Compra")
        if 'pedidos_concluido' in df.columns and 'categoria' in df.columns:
            df_abandono = df[df['pedidos_concluido'].str.lower().str.contains("nao")]
            abandono_por_categoria = df_abandono['categoria'].value_counts()
            fig = px.bar(abandono_por_categoria,
                         title="Quantidade de Abandonos por Categoria de Produto",
                         labels={"index": "Categoria", "value": "Qtd. Abandonos"})
            st.plotly_chart(fig, use_container_width=True)
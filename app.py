import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO GLOBAL DA APLICAÇÃO ---
st.set_page_config(
    page_title="Executive Business Intelligence | E-commerce Analytics",
    page_icon="⚡",
    layout="wide"
)

# --- 2. DESIGN SYSTEM & ESTILIZAÇÃO CORPORATIVA ---
st.markdown("""
    <style>
        div.metric-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            padding: 22px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
        }
        div.metric-card:hover {
            border-color: #58a6ff;
            box-shadow: 0 6px 16px rgba(88, 166, 255, 0.15);
            transform: translateY(-2px);
        }
        h1, h2, h3, p {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

ARQUIVO_DADOS = 'dados_limpos_dashboard.csv'

# --- 3. PIPELINE DE ENGENHARIA DE DADOS (ETL & AUTO-HEALING) ---
@st.cache_data(show_spinner=False)
def executar_pipeline_etl(caminho_csv):
    """
    Pipeline rigoroso de Ingestão, Limpeza e Tratamento de Dados (ETL).
    Executa auto-cura para gerar a base corporativa caso o arquivo não exista,
    assegurando integridade estrutural, eliminação de duplicidades e tipagem estrita.
    """
    if not os.path.exists(caminho_csv):
        np.random.seed(42)
        n_linhas = 5000
        estados = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE', 'CE', 'AM']
        categorias = ['Beleza e Saúde', 'Informática', 'Cama Mesa Banho', 'Esportes', 'Móveis', 'Eletrônicos']
        
        hoje = datetime.now()
        datas_compra = [hoje - timedelta(days=np.random.randint(0, 365)) for _ in range(n_linhas)]
        
        tempos_entrega = []
        estados_sorteados = np.random.choice(estados, n_linhas)
        for estado in estados_sorteados:
            if estado in ['AM', 'BA', 'PE', 'CE']:
                tempos_entrega.append(np.random.normal(18, 5))
            elif estado in ['SP', 'RJ', 'MG']:
                tempos_entrega.append(np.random.normal(5, 2))
            else:
                tempos_entrega.append(np.random.normal(10, 3))
                
        tempos_entrega = np.clip(tempos_entrega, 1, 45).astype(int)
        
        scores = []
        for tempo in tempos_entrega:
            prob = max(1, 5 - (tempo / 7))
            nota = np.random.normal(prob, 1)
            scores.append(np.clip(round(nota), 1, 5))
            
        df_temp = pd.DataFrame({
            'order_id': [f'ORD-{i:05d}' for i in range(n_linhas)],
            'order_purchase_timestamp': datas_compra,
            'customer_state': estados_sorteados,
            'product_category_name': np.random.choice(categorias, n_linhas),
            'price': np.round(np.random.uniform(50, 2000, n_linhas), 2),
            'delivery_time_days': tempos_entrega,
            'review_score': scores
        })
        df_temp.to_csv(caminho_csv, index=False)

    # Ingestão e Padronização de Colunas
    df = pd.read_csv(caminho_csv)
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.strip()
    
    # Conversão rigorosa de tipos de dados
    if 'order_purchase_timestamp' in df.columns:
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
        df['ano_mes'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['delivery_time_days'] = pd.to_numeric(df['delivery_time_days'], errors='coerce')
    df['review_score'] = pd.to_numeric(df['review_score'], errors='coerce')
    
    # Filtragem de integridade e eliminação de duplicidades por ID de pedido
    colunas_criticas = ['order_id', 'price', 'customer_state', 'product_category_name', 'review_score', 'delivery_time_days']
    df = df.dropna(subset=[c for c in colunas_criticas if c in df.columns])
    df = df.drop_duplicates(subset=['order_id'])
    
    # Validação lógica de negócio (exclusão estrita de prazos negativos)
    df = df[df['delivery_time_days'] >= 0]
    
    return df

# Carga segura do dataset processado
df = executar_pipeline_etl(ARQUIVO_DADOS)

# --- 4. BARRA LATERAL: GOVERNANÇA E FILTRAGEM ---
st.sidebar.title("Painel de Controle")
st.sidebar.markdown("Segmentação analítica da base de dados.")
st.sidebar.markdown("---")

estados_disponiveis = sorted(df['customer_state'].unique())
categorias_disponiveis = sorted(df['product_category_name'].unique())

estados_selecionados = st.sidebar.multiselect("Filtrar por Estado (UF):", options=estados_disponiveis, default=estados_disponiveis)
categorias_selecionadas = st.sidebar.multiselect("Filtrar por Categoria:", options=categorias_disponiveis, default=categorias_disponiveis)

# Proteção contra ausência de parâmetros nos filtros
if not estados_selecionados or not categorias_selecionadas:
    st.sidebar.warning("⚠️ Selecione ao menos um Estado e uma Categoria para atualizar as métricas executivas.")
    st.stop()

# Aplicação de filtros vetorizados via Pandas
df_filtrado = df[
    df['customer_state'].isin(estados_selecionados) & 
    df['product_category_name'].isin(categorias_selecionadas)
]

# --- 5. CABEÇALHO EXECUTIVO ---
st.title("⚡ Executive Intelligence | Faturamento e Séries Temporais")
st.markdown("Painel analítico corporativo para monitoramento estratégico do desempenho comercial e logístico.")
st.markdown("---")

# --- 6. INDICADORES EXECUTIVOS (KPIS) ---
col1, col2, col3, col4 = st.columns(4)

faturamento_total = df_filtrado['price'].sum()
volume_pedidos = len(df_filtrado)
tempo_medio_entrega = df_filtrado['delivery_time_days'].mean() if not df_filtrado.empty else 0
satisfacao_media = df_filtrado['review_score'].mean() if not df_filtrado.empty else 0

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <p style="color: #8b949e; margin: 0; font-size: 13px; font-weight: 600; text-transform: uppercase;">Faturamento Total</p>
            <h3 style="color: #58a6ff; margin: 8px 0 0 0; font-size: 24px;">R$ {faturamento_total:,.2f}</h3>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <p style="color: #8b949e; margin: 0; font-size: 13px; font-weight: 600; text-transform: uppercase;">Volume de Pedidos</p>
            <h3 style="color: #58a6ff; margin: 8px 0 0 0; font-size: 24px;">{volume_pedidos:,} un.</h3>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <p style="color: #8b949e; margin: 0; font-size: 13px; font-weight: 600; text-transform: uppercase;">Prazo Médio de Entrega</p>
            <h3 style="color: #58a6ff; margin: 8px 0 0 0; font-size: 24px;">{tempo_medio_entrega:.1f} dias</h3>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <p style="color: #8b949e; margin: 0; font-size: 13px; font-weight: 600; text-transform: uppercase;">Índice de Satisfação</p>
            <h3 style="color: #d29922; margin: 8px 0 0 0; font-size: 24px;">{satisfacao_media:.2f} / 5.0 ⭐</h3>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 7. VISUALIZAÇÕES E GRÁFICOS ANALÍTICOS (PLOTLY AVANÇADO) ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Top 10 Categorias por Faturamento")
    if not df_filtrado.empty:
        df_cat = df_filtrado.groupby('product_category_name')['price'].sum().reset_index()
        df_cat = df_cat.sort_values(by='price', ascending=True).tail(10)
        
        fig_cat = px.bar(
            df_cat,
            x='price',
            y='product_category_name',
            orientation='h',
            labels={'price': 'Faturamento Total (R$)', 'product_category_name': ''},
            color='price',
            color_continuous_scale='Tealgrn'
        )
        fig_cat.update_layout(
            template="plotly_dark", 
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    else:
        st.info("Nenhum registro encontrado para os critérios selecionados.")

with col_graf2:
    st.subheader("Evolução Temporal do Faturamento (Série Mensal)")
    if not df_filtrado.empty and 'ano_mes' in df_filtrado.columns:
        df_temporal = df_filtrado.groupby('ano_mes')['price'].sum().reset_index().sort_values('ano_mes')
        
        fig_line = px.line(
            df_temporal,
            x='ano_mes',
            y='price',
            markers=True,
            labels={'ano_mes': 'Período (Ano-Mês)', 'price': 'Faturamento Total (R$)'}
        )
        fig_line.update_traces(line_color='#58a6ff', line_width=3, marker=dict(size=8, color='#58a6ff'))
        fig_line.update_layout(
            template="plotly_dark", 
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#30363d'),
            yaxis=dict(showgrid=True, gridcolor='#30363d')
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Nenhum dado temporal encontrado para os critérios selecionados.")
import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

# Configuração da página
st.set_page_config(
    page_title="Dashboard Financeiro de Vendas",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== CONFIGURAÇÕES ====================
API_BASE_URL = "https://api.example.com"  # Substitua pela URL real da API
ENDPOINTS = {
    "vendas": "/api/vendas",
    "produtos": "/api/produtos",
    "clientes": "/api/clientes"
}

# ==================== FUNÇÕES DE API ====================
@st.cache_data(ttl=300)
def fetch_vendas(data_inicio=None, data_fim=None):
    """
    Busca dados de vendas da API.
    Para testes, retorna dados simulados.
    """
    try:
        # Para demonstração, usando dados simulados
        # Em produção, descomente e configure a URL real:
        # response = requests.get(f"{API_BASE_URL}{ENDPOINTS['vendas']}", timeout=10)
        # return response.json()
        
        return gerar_dados_vendas_simulados(data_inicio, data_fim)
    except Exception as e:
        st.error(f"Erro ao buscar vendas: {str(e)}")
        return []

@st.cache_data(ttl=300)
def fetch_clientes():
    """Busca dados de clientes da API."""
    try:
        return gerar_dados_clientes_simulados()
    except Exception as e:
        st.error(f"Erro ao buscar clientes: {str(e)}")
        return []

def gerar_dados_vendas_simulados(data_inicio=None, data_fim=None):
    """Gera dados simulados de vendas para demonstração."""
    import random
    import numpy as np
    
    if data_fim is None:
        data_fim = datetime.now()
    if data_inicio is None:
        data_inicio = data_fim - timedelta(days=90)
    
    datas = pd.date_range(start=data_inicio, end=data_fim, freq='D')
    vendas = []
    
    produtos = ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E']
    categorias = ['Eletrônicos', 'Alimentos', 'Vestuário', 'Serviços', 'Outros']
    regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    vendedores = ['Carlos', 'Maria', 'João', 'Ana', 'Pedro']
    
    for data in datas:
        for _ in range(random.randint(3, 15)):
            vendas.append({
                'data_venda': data,
                'id_venda': f"VND{int(data.timestamp())}{random.randint(1000, 9999)}",
                'produto': random.choice(produtos),
                'categoria': random.choice(categorias),
                'regiao': random.choice(regioes),
                'vendedor': random.choice(vendedores),
                'quantidade': random.randint(1, 20),
                'valor_unitario': round(random.uniform(10, 500), 2),
                'desconto_percentual': random.choice([0, 0, 0, 5, 10, 15]),
                'cliente': f"Cliente_{random.randint(1, 100)}",
                'status': random.choice(['Concluída', 'Pendente', 'Cancelada'])
            })
    
    df = pd.DataFrame(vendas)
    df['valor_total'] = df['quantidade'] * df['valor_unitario']
    df['desconto'] = df['valor_total'] * (df['desconto_percentual'] / 100)
    df['valor_liquido'] = df['valor_total'] - df['desconto']
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    
    return df

def gerar_dados_clientes_simulados():
    """Gera dados simulados de clientes."""
    clientes = []
    for i in range(1, 101):
        clientes.append({
            'id_cliente': i,
            'nome': f'Cliente_{i}',
            'regiao': ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'][i % 5],
            'tipo': ['PJ', 'PF'][i % 2],
            'ativo': i % 10 != 0
        })
    return pd.DataFrame(clientes)

# ==================== SIDEBAR ====================
st.sidebar.title("⚙️ Configurações")
st.sidebar.markdown("---")

# Filtros de data
col1, col2 = st.sidebar.columns(2)
with col1:
    data_inicio = st.date_input("Data Início", value=datetime.now() - timedelta(days=90))
with col2:
    data_fim = st.date_input("Data Fim", value=datetime.now())

# Carregar dados
vendas_df = fetch_vendas(data_inicio, data_fim)
clientes_df = fetch_clientes()

# Filtros adicionais
if not vendas_df.empty:
    regioes = ['Todas'] + sorted(vendas_df['regiao'].unique().tolist())
    regiao_selecionada = st.sidebar.selectbox("Região", regioes)
    
    categorias = ['Todas'] + sorted(vendas_df['categoria'].unique().tolist())
    categoria_selecionada = st.sidebar.selectbox("Categoria", categorias)
    
    status_vendas = ['Todas', 'Concluída', 'Pendente', 'Cancelada']
    status_selecionado = st.sidebar.selectbox("Status", status_vendas)

# ==================== APLICAR FILTROS ====================
vendas_filtradas = vendas_df.copy()

if regiao_selecionada != 'Todas':
    vendas_filtradas = vendas_filtradas[vendas_filtradas['regiao'] == regiao_selecionada]

if categoria_selecionada != 'Todas':
    vendas_filtradas = vendas_filtradas[vendas_filtradas['categoria'] == categoria_selecionada]

if status_selecionado != 'Todas':
    vendas_filtradas = vendas_filtradas[vendas_filtradas['status'] == status_selecionado]

# ==================== HEADER ====================
st.title("📊 Dashboard Financeiro de Vendas")
st.markdown("### Análise de Performance Empresarial para Gestores Financeiros")
st.markdown(f"Período: **{data_inicio.strftime('%d/%m/%Y')}** a **{data_fim.strftime('%d/%m/%Y')}**")
st.markdown("---")

# ==================== KPIs PRINCIPAIS ====================
if not vendas_filtradas.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    vendas_concluidas = vendas_filtradas[vendas_filtradas['status'] == 'Concluída']
    
    with col1:
        receita_total = vendas_concluidas['valor_liquido'].sum()
        st.metric(
            label="💰 Receita Total",
            value=f"R$ {receita_total:,.2f}",
            delta=f"R$ {receita_total * 0.1:,.2f} (+10%)",
            delta_color="off"
        )
    
    with col2:
        quantidade_vendas = len(vendas_concluidas)
        st.metric(
            label="🔢 Total de Vendas",
            value=quantidade_vendas,
            delta="3 vendas"
        )
    
    with col3:
        ticket_medio = vendas_concluidas['valor_liquido'].mean() if len(vendas_concluidas) > 0 else 0
        st.metric(
            label="🎯 Ticket Médio",
            value=f"R$ {ticket_medio:,.2f}",
            delta="-5%",
            delta_color="inverse"
        )
    
    with col4:
        margem_lucro = ((vendas_concluidas['valor_liquido'].sum() / vendas_concluidas['valor_total'].sum() * 100) 
                       if vendas_concluidas['valor_total'].sum() > 0 else 0)
        st.metric(
            label="📈 Margem de Lucro",
            value=f"{margem_lucro:.1f}%",
            delta="+2%"
        )

st.markdown("---")

# ==================== GRÁFICOS PRINCIPAIS ====================

Aba1, Aba2, Aba3 = st.tabs(["Vendas", "Performace", "Detalhes"])

with Aba1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Vendas por Dia")
        vendas_por_dia = vendas_filtradas[vendas_filtradas['status'] == 'Concluída'].groupby(
            vendas_filtradas['data_venda'].dt.date
        )['valor_liquido'].agg(['sum', 'count']).reset_index()
        vendas_por_dia.columns = ['Data', 'Receita', 'Quantidade']
        
        fig_linha = go.Figure()
        fig_linha.add_trace(go.Scatter(
            x=vendas_por_dia['Data'],
            y=vendas_por_dia['Receita'],
            mode='lines+markers',
            name='Receita',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6)
        ))
        fig_linha.update_layout(
            hovermode='x unified',
            height=400,
            template='plotly_white',
            xaxis_title='Data',
            yaxis_title='Receita (R$)'
        )
        st.plotly_chart(fig_linha, use_container_width=True)

    with col2:
        st.subheader("💼 Vendas por Categoria")
        vendas_categoria = vendas_filtradas[vendas_filtradas['status'] == 'Concluída'].groupby(
            'categoria'
        )['valor_liquido'].sum().sort_values(ascending=False)
        
        fig_pizza = go.Figure(data=[go.Pie(
            labels=vendas_categoria.index,
            values=vendas_categoria.values,
            hovertemplate='<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}',
            marker=dict(
                colors=px.colors.qualitative.Set2
            )
        )])
        fig_pizza.update_layout(height=400)
        st.plotly_chart(fig_pizza, use_container_width=True)

# ==================== ANÁLISE POR REGIÃO ====================
with Aba2:
    st.subheader("🗺️ Performance por Região")
    col1, col2 = st.columns(2)

    with col1:
        vendas_regiao = vendas_filtradas[vendas_filtradas['status'] == 'Concluída'].groupby(
            'regiao'
        ).agg({
            'valor_liquido': 'sum',
            'id_venda': 'count'
        }).reset_index()
        vendas_regiao.columns = ['Região', 'Receita', 'Quantidade']
        vendas_regiao = vendas_regiao.sort_values('Receita', ascending=True)
        
        fig_barra = go.Figure(data=[
            go.Bar(
                y=vendas_regiao['Região'],
                x=vendas_regiao['Receita'],
                orientation='h',
                marker=dict(color='#ff7f0e'),
                text=vendas_regiao['Receita'].apply(lambda x: f'R$ {x:,.0f}'),
                textposition='auto'
            )
        ])
        fig_barra.update_layout(
            height=300,
            template='plotly_white',
            xaxis_title='Receita (R$)',
            yaxis_title='Região'
        )
        st.plotly_chart(fig_barra, use_container_width=True)

    with col2:
        vendas_vendedor = vendas_filtradas[vendas_filtradas['status'] == 'Concluída'].groupby(
            'vendedor'
        ).agg({
            'valor_liquido': 'sum',
            'id_venda': 'count'
        }).reset_index()
        vendas_vendedor.columns = ['Vendedor', 'Receita', 'Quantidade']
        vendas_vendedor = vendas_vendedor.sort_values('Receita', ascending=False).head(10)
        
        fig_vendedor = px.bar(
            vendas_vendedor,
            x='Vendedor',
            y='Receita',
            color='Quantidade',
            title='Top 10 Vendedores',
            color_continuous_scale='Viridis'
        )
        fig_vendedor.update_layout(height=300, template='plotly_white')
        st.plotly_chart(fig_vendedor, use_container_width=True)

# ==================== TABELA DE VENDAS DETALHADAS ====================
with Aba3:
    st.markdown("---")
    st.subheader("📋 Detalhamento de Vendas")

    if not vendas_filtradas.empty:
        # Preparar dados para exibição
        vendas_exibicao = vendas_filtradas.copy()
        vendas_exibicao['data_venda'] = vendas_exibicao['data_venda'].dt.strftime('%d/%m/%Y')
        vendas_exibicao['valor_unitario'] = vendas_exibicao['valor_unitario'].apply(lambda x: f'R$ {x:.2f}')
        vendas_exibicao['valor_total'] = vendas_exibicao['valor_total'].apply(lambda x: f'R$ {x:,.2f}')
        vendas_exibicao['desconto'] = vendas_exibicao['desconto'].apply(lambda x: f'R$ {x:,.2f}')
        vendas_exibicao['valor_liquido'] = vendas_exibicao['valor_liquido'].apply(lambda x: f'R$ {x:,.2f}')
        
        # Selecionar colunas para exibição
        colunas_exibicao = ['data_venda', 'id_venda', 'vendedor', 'cliente', 'produto', 
                            'categoria', 'regiao', 'quantidade', 'valor_unitario', 
                            'valor_total', 'desconto', 'valor_liquido', 'status']
        
        vendas_exibicao = vendas_exibicao[colunas_exibicao]
        vendas_exibicao.columns = ['Data', 'ID Venda', 'Vendedor', 'Cliente', 'Produto', 
                                'Categoria', 'Região', 'Qtd', 'Valor Unit.', 
                                'Valor Total', 'Desconto', 'Valor Líquido', 'Status']
        
        st.dataframe(
            vendas_exibicao.sort_values('Data', ascending=False),
            use_container_width=True,
            height=500
        )
    else:
        st.warning("Nenhuma venda encontrada com os filtros selecionados.")

    # ==================== ANÁLISE COMPARATIVA ====================
    st.markdown("---")
    st.subheader("📊 Análise Comparativa")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Status das Vendas**")
        status_count = vendas_filtradas['status'].value_counts()
        
        fig_status = go.Figure(data=[go.Bar(
            x=status_count.index,
            y=status_count.values,
            marker=dict(color=['#2ecc71', '#f39c12', '#e74c3c']),
            text=status_count.values,
            textposition='auto'
        )])
        fig_status.update_layout(
            height=300,
            template='plotly_white',
            xaxis_title='Status',
            yaxis_title='Quantidade'
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with col2:
        st.write("**Produtos Mais Vendidos**")
        produtos_top = vendas_filtradas[vendas_filtradas['status'] == 'Concluída'].groupby(
            'produto'
        )['id_venda'].count().sort_values(ascending=False).head(5)
        
        fig_produtos = go.Figure(data=[go.Bar(
            x=produtos_top.values,
            y=produtos_top.index,
            orientation='h',
            marker=dict(color='#3498db'),
            text=produtos_top.values,
            textposition='auto'
        )])
        fig_produtos.update_layout(
            height=300,
            template='plotly_white',
            xaxis_title='Quantidade de Vendas',
            yaxis_title='Produto'
        )
        st.plotly_chart(fig_produtos, use_container_width=True)

    # ==================== RESUMO EXECUTIVO ====================
    st.markdown("---")
    st.subheader("📌 Resumo Executivo")

    resumo_col1, resumo_col2, resumo_col3 = st.columns(3)

    with resumo_col1:
        st.info(f"""
        **Período Analisado:**
        - De: {data_inicio.strftime('%d/%m/%Y')}
        - Até: {data_fim.strftime('%d/%m/%Y')}
        """)

    with resumo_col2:
        st.success(f"""
        **Melhores Resultados:**
        - Região: {vendas_filtradas.groupby('regiao')['valor_liquido'].sum().idxmax() if not vendas_filtradas.empty else 'N/A'}
        - Categoria: {vendas_filtradas.groupby('categoria')['valor_liquido'].sum().idxmax() if not vendas_filtradas.empty else 'N/A'}
        """)

    with resumo_col3:
        taxa_concluida = (len(vendas_filtradas[vendas_filtradas['status'] == 'Concluída']) / len(vendas_filtradas) * 100 
                        if len(vendas_filtradas) > 0 else 0)
        st.warning(f"""
        **Indicadores:**
        - Taxa de Conclusão: {taxa_concluida:.1f}%
        - Total de Transações: {len(vendas_filtradas)}
        """)

st.markdown("---")
st.caption("Dashboard atualizado automaticamente a cada 5 minutos. Desenvolvido para análise financeira.")

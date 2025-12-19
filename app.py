"""
Dashboard Streamlit - Análise de Extratos Bancários
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import base64

# Configuração da página
st.set_page_config(
    page_title="Dashboard - Análise de Extratos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
    h1 {
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Caminhos
SAIDA_DIR = Path("saida_analise")
GRAFICOS_DIR = SAIDA_DIR / "graficos"

# Função para verificar arquivos
def verificar_dados():
    """Verifica se os dados foram gerados"""
    if not SAIDA_DIR.exists():
        return False, "Pasta saida_analise não encontrada"
    
    arquivos_necessarios = [
        "08_indicadores.csv",
        "03_fluxo_caixa_mensal.csv",
        "04_saidas_por_categoria.csv",
        "05_entradas_por_categoria.csv"
    ]
    
    for arquivo in arquivos_necessarios:
        if not (SAIDA_DIR / arquivo).exists():
            return False, f"Arquivo {arquivo} não encontrado"
    
    return True, "OK"

# Função para carregar dados
@st.cache_data
def carregar_dados():
    """Carrega todos os dados CSV"""
    dados = {}
    
    try:
        dados['indicadores'] = pd.read_csv(SAIDA_DIR / "08_indicadores.csv", sep=";", decimal=",")
        dados['fluxo'] = pd.read_csv(SAIDA_DIR / "03_fluxo_caixa_mensal.csv", sep=";", decimal=",")
        dados['saidas_cat'] = pd.read_csv(SAIDA_DIR / "04_saidas_por_categoria.csv", sep=";", decimal=",")
        dados['entradas_cat'] = pd.read_csv(SAIDA_DIR / "05_entradas_por_categoria.csv", sep=";", decimal=",")
        dados['resumo'] = pd.read_csv(SAIDA_DIR / "01_resumo_mensal.csv", sep=";", decimal=",")
        dados['transacoes'] = pd.read_csv(SAIDA_DIR / "02_movimentacoes.csv", sep=";", decimal=",")
        
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

# Função para exibir imagem
def mostrar_grafico(nome_arquivo):
    """Exibe um gráfico PNG"""
    caminho = GRAFICOS_DIR / nome_arquivo
    if caminho.exists():
        st.image(str(caminho), use_container_width=True)
    else:
        st.warning(f"Gráfico {nome_arquivo} não encontrado")

# Header
st.title("📊 Dashboard - Análise de Extratos Bancários")
st.markdown("### Itaú PJ - Janeiro a Novembro 2025")
st.markdown("---")

# Verificar dados
dados_ok, mensagem = verificar_dados()

if not dados_ok:
    st.error(f"⚠️ {mensagem}")
    st.info("""
    **Como gerar os dados:**
    1. Coloque os PDFs na pasta `pdfs/`
    2. Execute: `python -m src.main`
    3. Atualize esta página
    """)
    st.stop()

# Carregar dados
dados = carregar_dados()

if dados is None:
    st.stop()

# Extrair valores dos indicadores
indicadores_dict = dict(zip(dados['indicadores']['Indicador'], dados['indicadores']['Valor']))

total_entradas = indicadores_dict.get('Total de Entradas', 0)
total_saidas = indicadores_dict.get('Total de Saídas', 0)
resultado = indicadores_dict.get('Resultado Líquido', 0)
media_mensal = indicadores_dict.get('Média Mensal de Entradas', 0)
num_meses = int(indicadores_dict.get('Número de Meses', 0))

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total de Entradas",
        value=f"R$ {total_entradas:,.2f}",
        delta=f"{num_meses} meses"
    )

with col2:
    st.metric(
        label="💸 Total de Saídas",
        value=f"R$ {total_saidas:,.2f}",
        delta=f"{len(dados['transacoes'])} transações"
    )

with col3:
    st.metric(
        label="📊 Resultado Líquido",
        value=f"R$ {resultado:,.2f}",
        delta="Déficit" if resultado < 0 else "Superávit",
        delta_color="inverse" if resultado < 0 else "normal"
    )

with col4:
    st.metric(
        label="📈 Média Mensal",
        value=f"R$ {media_mensal:,.2f}",
        delta="Entradas"
    )

st.markdown("---")

# Tabs para organizar conteúdo
tab1, tab2, tab3, tab4 = st.tabs(["📈 Visão Geral", "📊 Análise Detalhada", "📋 Dados", "ℹ️ Sobre"])

with tab1:
    st.header("Visão Geral")
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Entradas por Mês")
        mostrar_grafico("entradas_por_mes.png")
    
    with col2:
        st.subheader("📉 Saídas por Mês")
        mostrar_grafico("saidas_por_mes.png")
    
    # Resultado
    st.subheader("💰 Resultado Líquido por Mês")
    mostrar_grafico("resultado_por_mes.png")

with tab2:
    st.header("Análise Detalhada")
    
    # Top categorias
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔴 Top 10 Categorias - Saídas")
        mostrar_grafico("top10_categorias_saida.png")
        
        # Tabela
        st.dataframe(
            dados['saidas_cat'].head(10),
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.subheader("🟢 Top 10 Categorias - Entradas")
        mostrar_grafico("top10_categorias_entrada.png")
        
        # Tabela
        st.dataframe(
            dados['entradas_cat'].head(10),
            use_container_width=True,
            hide_index=True
        )
    
    # Pareto
    st.subheader("📊 Análise de Pareto - Saídas por Categoria")
    mostrar_grafico("pareto_saidas_categoria.png")

with tab3:
    st.header("Dados Completos")
    
    # Seletor de dados
    tipo_dado = st.selectbox(
        "Selecione o tipo de dado:",
        ["Fluxo de Caixa Mensal", "Resumo Mensal", "Transações", "Saídas por Categoria", "Entradas por Categoria"]
    )
    
    if tipo_dado == "Fluxo de Caixa Mensal":
        st.dataframe(dados['fluxo'], use_container_width=True, hide_index=True)
        
    elif tipo_dado == "Resumo Mensal":
        st.dataframe(dados['resumo'], use_container_width=True, hide_index=True)
        
    elif tipo_dado == "Transações":
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            categorias = ["Todas"] + list(dados['transacoes']['categoria'].unique())
            cat_selecionada = st.selectbox("Filtrar por categoria:", categorias)
        
        with col2:
            meses = ["Todos"] + list(dados['transacoes']['mes_key'].dropna().unique())
            mes_selecionado = st.selectbox("Filtrar por mês:", meses)
        
        # Aplicar filtros
        df_filtrado = dados['transacoes'].copy()
        if cat_selecionada != "Todas":
            df_filtrado = df_filtrado[df_filtrado['categoria'] == cat_selecionada]
        if mes_selecionado != "Todos":
            df_filtrado = df_filtrado[df_filtrado['mes_key'] == mes_selecionado]
        
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
        st.info(f"Mostrando {len(df_filtrado)} de {len(dados['transacoes'])} transações")
        
    elif tipo_dado == "Saídas por Categoria":
        st.dataframe(dados['saidas_cat'], use_container_width=True, hide_index=True)
        
    elif tipo_dado == "Entradas por Categoria":
        st.dataframe(dados['entradas_cat'], use_container_width=True, hide_index=True)
    
    # Botão de download
    st.markdown("---")
    st.subheader("📥 Download")
    
    excel_path = SAIDA_DIR / "analise_extratos.xlsx"
    if excel_path.exists():
        with open(excel_path, 'rb') as f:
            st.download_button(
                label="📥 Baixar Análise Completa (Excel)",
                data=f,
                file_name="analise_extratos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

with tab4:
    st.header("ℹ️ Sobre o Sistema")
    
    st.markdown("""
    ### 📊 Sistema de Análise de Extratos Bancários
    
    Este dashboard apresenta a análise automatizada de extratos bancários do **Itaú PJ**.
    
    #### 🎯 Funcionalidades:
    - ✅ Extração automática de dados de PDFs
    - ✅ Categorização inteligente de transações
    - ✅ Análises consolidadas e gráficos
    - ✅ Exportação para Excel e CSV
    
    #### 📈 Período Analisado:
    - **Janeiro a Novembro de 2025**
    - **11 meses** de dados
    - **581 transações** processadas
    - **6 categorias** principais identificadas
    
    #### 🔧 Tecnologias Utilizadas:
    - Python 3.12
    - Streamlit
    - pdfplumber
    - pandas
    - matplotlib
    
    #### 📝 Categorias Automáticas:
    - Fornecedores
    - Tributos/Boletos
    - PIX
    - Cartões
    - Tarifas Bancárias
    - Débito Automático
    - Saques
    - Depósitos
    - Aplicações/Resgates
    - Transferências
    - Recebimentos
    - Outros
    
    ---
    
    **Desenvolvido com ❤️ para análise financeira**
    """)
    
    # Estatísticas adicionais
    st.subheader("📊 Estatísticas do Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("PDFs Processados", f"{num_meses}")
        
    with col2:
        st.metric("Transações", f"{len(dados['transacoes'])}")
        
    with col3:
        st.metric("Categorias", f"{len(dados['saidas_cat'])}")

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/streamlit/streamlit/develop/docs/logo.png", width=100)
    st.title("Menu")
    
    st.markdown("---")
    
    st.subheader("📊 Resumo Rápido")
    st.metric("Período", f"{num_meses} meses")
    st.metric("Transações", len(dados['transacoes']))
    
    st.markdown("---")
    
    st.subheader("🔄 Atualizar Dados")
    if st.button("🔄 Reprocessar Análise"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    
    st.caption("Dashboard v1.0")
    st.caption("Última atualização: 19/12/2025")

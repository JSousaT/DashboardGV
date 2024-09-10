import streamlit as st
import pandas as pd
import plotly.express as px

# Função para carregar os dados do Excel
def ler_dados_excel():
    # Substituir pelo caminho real do arquivo
    file_path = r"U:\Analise\2024\Campanha\CampanhaSC\PBI\SC\ProLista_TotalFech.xlsx"
    df = pd.read_excel(file_path, engine='openpyxl')

    # Garantir que as colunas relevantes são numéricas
    df['% VarVB'] = pd.to_numeric(df['% VarVB'], errors='coerce')
    df['Desvio POS'] = pd.to_numeric(df['Desvio POS'], errors='coerce')
    df['Real VB'] = pd.to_numeric(df['Real VB'], errors='coerce')
    df['Devol VB'] = pd.to_numeric(df['Devol VB'], errors='coerce')
    return df

# Função para criar gráficos de análise para um GV específico
def criar_graficos(df_gv, gv):
    st.title(f"Análise para {gv}")

    # Gráfico 1: Variação de Vendas Brutas (% VarVB)
    fig1 = px.bar(df_gv, x='Nome Linha', y='% VarVB', title="Variação de Vendas Brutas (%)")
    st.plotly_chart(fig1)

    # Gráfico 2: Desvio POS
    fig2 = px.bar(df_gv, x='Nome Linha', y='Desvio POS', title="Desvio de POS")
    st.plotly_chart(fig2)

    # Gráfico 3: Real VB vs Devoluções VB
    fig3 = px.bar(df_gv, x='Nome Linha', y=['Real VB', 'Devol VB'], title="Vendas Brutas vs Devoluções")
    st.plotly_chart(fig3)

    # Gráfico 4: Meta POS vs Real POS
    fig4 = px.bar(df_gv, x='Nome Linha', y=['Meta POS.', 'Real POS.'], title="Meta POS vs Real POS")
    st.plotly_chart(fig4)

# Função para configurar o dashboard e gerar os gráficos para cada GV
def configurar_dashboard(df):
    # Obter o parâmetro de GV da URL
    query_params = st.experimental_get_query_params()
    gv_selecionado = query_params.get("gv", [None])[0]

    # Verificar se o GV foi passado via URL, caso contrário, selecionar na sidebar
    if gv_selecionado:
        st.sidebar.write(f"Gerente selecionado via URL: {gv_selecionado}")
    else:
        st.sidebar.title("Selecione o Gerente Regional (GV)")
        gerentes = df['NOME'].unique()
        gv_selecionado = st.sidebar.selectbox("Gerente Regional", gerentes)

    # Gerar gráficos para o GV selecionado
    if gv_selecionado:
        df_gv = df[df['NOME'] == gv_selecionado]
        criar_graficos(df_gv, gv_selecionado)

# Carregar os dados
df = ler_dados_excel()

# Configurar o dashboard e gerar os gráficos
configurar_dashboard(df)

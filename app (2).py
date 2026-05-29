import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta
import io

# Configuração da página
st.set_page_config(
    page_title="Gantt Corporativo - Gestão de Atividades",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização CSS personalizada para Design Totalmente Claro e Moderno
st.markdown("""
    <style>
    /* Fundo principal claro */
    .stApp {
        background-color: #fcfcfc;
    }
    
    /* Customização das abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #ffffff;
        padding: 10px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        color: #666;
        font-weight: 600;
        font-size: 16px;
    }

    .stTabs [aria-selected="true"] {
        color: #007bff !important;
        border-bottom: 2px solid #007bff !important;
    }

    /* Cards de Indicadores */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        text-align: center;
    }
    
    /* Estilo para inputs e botões */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 45px;
        font-weight: 600;
    }
    
    /* Gráfico e Tabelas */
    .plot-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.04);
        border: 1px solid #f0f0f0;
    }
    
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Inter', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE DADOS ---

def get_default_data():
    """Dados iniciais com os novos campos obrigatórios."""
    data = {
        'PREFIXO': ['PRJ-001', 'PRJ-001', 'PRJ-002', 'PRJ-003', 'PRJ-001'],
        'PEÇA': ['Eixo Principal', 'Suporte Lateral', 'Engrenagem A', 'Base Estrutural', 'Tampa Protetora'],
        'DATA INÍCIO': [date(2026, 5, 1), date(2026, 5, 5), date(2026, 5, 10), date(2026, 5, 15), date(2026, 5, 20)],
        'DATA FIM': [date(2026, 5, 10), date(2026, 5, 15), date(2026, 5, 25), date(2026, 6, 5), date(2026, 5, 28)],
        'AÇÃO': ['Usinagem', 'Pintura', 'Montagem', 'Soldagem', 'Inspeção'],
        'STATUS': ['Concluído', 'Em Andamento', 'Pendente', 'Em Andamento', 'Atrasado'],
        'PROGRESSO': [100, 60, 0, 45, 10],
        'OBSERVAÇÃO': ['Finalizado com sucesso.', 'Aguardando secagem.', 'Peça em estoque.', 'Iniciando solda mig.', 'Atraso no fornecedor.']
    }
    return pd.DataFrame(data)

# No Streamlit Cloud, o session_state limpa ao fechar a aba. 
# Para persistência real entre usuários, seria necessário um banco de dados.
if 'df' not in st.session_state:
    st.session_state.df = get_default_data()

# --- INTERFACE PRINCIPAL ---

st.title("📊 Gestão de Atividades Corporativas")

tab1, tab2 = st.tabs(["📈 Dashboard & Gráfico de Gantt", "📝 Cadastro & Preenchimento"])

# --- ABA 1: DASHBOARD & GANTT ---
with tab1:
    # 1. Dashboard de Indicadores Superiores
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Atividades", len(st.session_state.df))
    with col2:
        st.metric("Concluídas", len(st.session_state.df[st.session_state.df['STATUS'] == 'Concluído']))
    with col3:
        st.metric("Em Andamento", len(st.session_state.df[st.session_state.df['STATUS'] == 'Em Andamento']))
    with col4:
        st.metric("Atrasadas", len(st.session_state.df[st.session_state.df['STATUS'] == 'Atrasado']))
    with col5:
        avg_prog = st.session_state.df['PROGRESSO'].mean() if not st.session_state.df.empty else 0
        st.metric("Progresso Médio", f"{avg_prog:.1f}%")

    st.divider()

    # 2. Área de Filtros Próximos ao Gráfico
    st.subheader("🔍 Filtros Dinâmicos")
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    with f_col1:
        prefixos = ["Todos"] + sorted(st.session_state.df['PREFIXO'].unique().tolist())
        sel_prefixo = st.selectbox("Filtrar por Prefixo", prefixos)
    
    with f_col2:
        status_list = ["Todos"] + sorted(st.session_state.df['STATUS'].unique().tolist())
        sel_status = st.selectbox("Filtrar por Status", status_list)
        
    with f_col3:
        acoes = ["Todos"] + sorted(st.session_state.df['AÇÃO'].unique().tolist())
        sel_acao = st.selectbox("Filtrar por Ação", acoes)
        
    with f_col4:
        date_range = st.date_input("Filtrar por Período", [
            st.session_state.df['DATA INÍCIO'].min(),
            st.session_state.df['DATA FIM'].max()
        ])

    # Aplicar Filtros
    df_filtered = st.session_state.df.copy()
    if sel_prefixo != "Todos":
        df_filtered = df_filtered[df_filtered['PREFIXO'] == sel_prefixo]
    if sel_status != "Todos":
        df_filtered = df_filtered[df_filtered['STATUS'] == sel_status]
    if sel_acao != "Todos":
        df_filtered = df_filtered[df_filtered['AÇÃO'] == sel_acao]
    
    if len(date_range) == 2:
        start_d, end_d = date_range[0], date_range[1]
        df_filtered = df_filtered[(df_filtered['DATA INÍCIO'] >= start_d) & (df_filtered['DATA FIM'] <= end_d)]

    st.divider()

    # 3. Gráfico de Gantt
    st.subheader("📅 Cronograma (Gantt)")
    
    if not df_filtered.empty:
        # Preparar dados para o Gantt
        df_gantt = df_filtered.copy()
        # Concatenar informações para o eixo Y conforme solicitado (Prefixo - Peça)
        df_gantt['Identificador'] = df_gantt['PREFIXO'] + " | " + df_gantt['PEÇA']
        
        # Mapeamento de Cores Profissionais
        color_map = {
            'Concluído': '#2ECC71',     # Verde suave
            'Em Andamento': '#3498DB',  # Azul corporativo
            'Pendente': '#F1C40F',      # Amarelo suave
            'Atrasado': '#E74C3C'       # Vermelho suave
        }

        fig = px.timeline(
            df_gantt,
            x_start="DATA INÍCIO",
            x_end="DATA FIM",
            y="Identificador",
            color="STATUS",
            hover_data=["PREFIXO", "PEÇA", "AÇÃO", "STATUS", "PROGRESSO"],
            color_discrete_map=color_map,
            text="PROGRESSO", # Mostrar progresso na barra
            opacity=0.9
        )
        
        fig.update_yaxes(autorange="reversed", title="")
        fig.update_xaxes(title="Linha do Tempo")
        
        # Adicionar linha do dia atual
        today = datetime.now()
        fig.add_vline(x=today.timestamp() * 1000, line_width=2, line_dash="dash", line_color="#34495E", annotation_text="Hoje")

        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            uniformtext_mode='hide',
            uniformtext_minsize=10
        )
        
        # Ajustar o texto do progresso dentro das barras
        fig.update_traces(
            texttemplate='%{text}%', 
            textposition='inside', 
            insidetextanchor='middle',
            marker_line_color='white',
            marker_line_width=1
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Nenhum dado encontrado para os filtros aplicados.")

# --- ABA 2: CADASTRO & PREENCHIMENTO ---
with tab2:
    st.subheader("📝 Cadastro e Edição de Atividades")
    st.info("Utilize a tabela abaixo para cadastrar novas peças ou editar as existentes. Clique em 'Salvar' para atualizar o gráfico.")
    
    # Editor de dados interativo
    edited_df = st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "PREFIXO": st.column_config.TextColumn("PREFIXO", help="Código do projeto ou lote"),
            "PEÇA": st.column_config.TextColumn("PEÇA", help="Nome da peça ou componente"),
            "DATA INÍCIO": st.column_config.DateColumn("DATA INÍCIO", format="DD/MM/YYYY"),
            "DATA FIM": st.column_config.DateColumn("DATA FIM", format="DD/MM/YYYY"),
            "AÇÃO": st.column_config.TextColumn("AÇÃO", help="Atividade a ser realizada"),
            "STATUS": st.column_config.SelectboxColumn(
                "STATUS",
                options=["Pendente", "Em Andamento", "Concluído", "Atrasado"],
                required=True
            ),
            "PROGRESSO": st.column_config.NumberColumn(
                "PROGRESSO (%)",
                min_value=0,
                max_value=100,
                format="%d%%",
                help="Informe o percentual de conclusão (0-100)"
            ),
            "OBSERVAÇÃO": st.column_config.TextColumn("OBSERVAÇÃO")
        },
        key="data_editor_v2"
    )
    
    col_save1, col_save2, col_save3 = st.columns([1, 1, 1])
    with col_save2:
        if st.button("💾 Salvar Alterações"):
            st.session_state.df = edited_df
            st.success("Dados atualizados com sucesso! Vá para a aba Dashboard para ver o gráfico.")
            st.rerun()

    st.divider()
    
    # Seção de Importação/Exportação na aba de Cadastro
    st.subheader("📥 Ferramentas de Dados")
    exp_col1, exp_col2 = st.columns(2)
    
    with exp_col1:
        uploaded_file = st.file_uploader("Importar Planilha Excel (.xlsx)", type=["xlsx"])
        if uploaded_file:
            try:
                import_df = pd.read_excel(uploaded_file)
                # Validar colunas
                required_cols = ['PREFIXO', 'PEÇA', 'DATA INÍCIO', 'DATA FIM', 'AÇÃO', 'STATUS', 'PROGRESSO', 'OBSERVAÇÃO']
                if all(col in import_df.columns for col in required_cols):
                    import_df['DATA INÍCIO'] = pd.to_datetime(import_df['DATA INÍCIO']).dt.date
                    import_df['DATA FIM'] = pd.to_datetime(import_df['DATA FIM']).dt.date
                    st.session_state.df = import_df
                    st.success("Dados importados com sucesso!")
                    st.rerun()
                else:
                    st.error(f"O arquivo deve conter as colunas: {', '.join(required_cols)}")
            except Exception as e:
                st.error(f"Erro ao processar arquivo: {e}")
                
    with exp_col2:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.df.to_excel(writer, index=False, sheet_name='Atividades')
        
        st.download_button(
            label="📥 Exportar para Excel",
            data=buffer.getvalue(),
            file_name=f"gestao_gantt_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.caption("Sistema de Gestão de Projetos - Visual Corporativo Clean v2.0")

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import io

# Configuração da página
st.set_page_config(
    page_title="PCP Moderno - Gestão de Atividades",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS PARA FORÇAR TEMA CLARO E TABELA LEGÍVEL
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    /* Fundo Branco em Tudo */
    .stApp, [data-testid="stHeader"], [data-testid="stSidebar"], .main {
        background-color: #ffffff !important;
    }

    /* Texto Preto em Tudo */
    h1, h2, h3, p, span, label, .stMarkdown, .stSelectbox, .stMultiSelect {
        color: #000000 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Tabela de Edição (Forçar Fundo Claro e Texto Preto) */
    [data-testid="stDataEditor"] {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 12px !important;
    }
    
    /* Forçar cores dos botões de Salvar, Importar e Exportar */
    .stButton>button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        height: 50px !important;
    }

    /* Cards de Indicadores */
    .metric-card {
        background-color: #ffffff !important;
        border: 1px solid #f0f0f0 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        text-align: center;
    }

    /* Estilo das Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #f8fafc;
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        padding: 8px 20px;
        color: #64748b !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #2563eb !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS ---
def get_data():
    return pd.DataFrame({
        'PREFIXO': ['LOTE-01', 'LOTE-01', 'LOTE-02', 'LOTE-03', 'LOTE-01'],
        'PEÇA': ['Eixo Principal', 'Suporte Base', 'Engrenagem Z', 'Painel Frontal', 'Válvula 40'],
        'DATA INÍCIO': [date(2026, 5, 1), date(2026, 5, 4), date(2026, 5, 10), date(2026, 5, 15), date(2026, 5, 20)],
        'DATA FIM': [date(2026, 5, 12), date(2026, 5, 15), date(2026, 5, 25), date(2026, 6, 5), date(2026, 5, 28)],
        'AÇÃO': ['Usinagem', 'Pintura', 'Montagem', 'Soldagem', 'Inspeção'],
        'STATUS': ['Concluído', 'Em Andamento', 'Pendente', 'Em Andamento', 'Atrasado'],
        'PROGRESSO': [100, 65, 0, 40, 15],
        'OBSERVAÇÃO': ['OK', 'Secagem', 'Peças', 'Turno 2', 'Fornecedor']
    })

if 'df' not in st.session_state:
    st.session_state.df = get_data()

# --- HEADER ---
st.title("🚀 Reunião de Planejamento Semanal PCP")

tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Gantt", "✅ Atividades Concluídas", "⚙️ Cadastro e Edição"])

# --- ABA 1: DASHBOARD ---
with tab1:
    m1, m2, m3, m4 = st.columns(4)
    df_active = st.session_state.df[st.session_state.df['STATUS'] != 'Concluído']
    
    with m1: st.markdown(f'<div class="metric-card"><b>Total Atividades</b><br><span style="font-size: 28px; font-weight: 800;">{len(st.session_state.df)}</span></div>', unsafe_allow_html=True)
    with m2: 
        v = len(st.session_state.df[st.session_state.df['STATUS'] == 'Em Andamento'])
        st.markdown(f'<div class="metric-card" style="border-top: 4px solid #3b82f6;"><b>Em Andamento</b><br><span style="font-size: 28px; font-weight: 800; color: #3b82f6;">{v}</span></div>', unsafe_allow_html=True)
    with m3: 
        v = len(st.session_state.df[st.session_state.df['STATUS'] == 'Atrasado'])
        st.markdown(f'<div class="metric-card" style="border-top: 4px solid #ef4444;"><b>Atrasadas</b><br><span style="font-size: 28px; font-weight: 800; color: #ef4444;">{v}</span></div>', unsafe_allow_html=True)
    with m4: 
        v = st.session_state.df['PROGRESSO'].mean()
        st.markdown(f'<div class="metric-card" style="border-top: 4px solid #8b5cf6;"><b>Progresso Médio</b><br><span style="font-size: 28px; font-weight: 800; color: #8b5cf6;">{v:.0f}%</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filtros
    with st.expander("🔍 Filtros de Visualização", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1: s_pref = st.multiselect("Prefixos", options=sorted(st.session_state.df['PREFIXO'].unique()), default=sorted(st.session_state.df['PREFIXO'].unique()))
        with f2: s_stat = st.multiselect("Status", options=["Pendente", "Em Andamento", "Atrasado"], default=["Pendente", "Em Andamento", "Atrasado"])
        with f3: per = st.date_input("Período", [st.session_state.df['DATA INÍCIO'].min(), st.session_state.df['DATA FIM'].max()])

    # Plotagem (Apenas Ativas)
    df_p = st.session_state.df[st.session_state.df['STATUS'] != 'Concluído'].copy()
    df_p = df_p[df_p['PREFIXO'].isin(s_pref)]
    df_p = df_p[df_p['STATUS'].isin(s_stat)]
    
    if not df_p.empty:
        df_p['ID'] = df_p['PREFIXO'] + " - " + df_p['PEÇA']
        colors = {'Em Andamento': '#3b82f6', 'Pendente': '#f59e0b', 'Atrasado': '#ef4444'}
        fig = px.timeline(df_p, x_start="DATA INÍCIO", x_end="DATA FIM", y="ID", color="STATUS", color_discrete_map=colors, text="PROGRESSO")
        fig.update_xaxes(tickformat="%d/%b\n(Sem %V)", dtick="D7", gridcolor='#f1f5f9')
        fig.update_yaxes(autorange="reversed", title="", gridcolor='#f1f5f9')
        fig.add_vline(x=datetime.now().timestamp()*1000, line_width=3, line_color="#000", annotation_text="HOJE")
        fig.update_layout(height=600, plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=10, r=10, t=50, b=10))
        fig.update_traces(texttemplate='%{text}%', textposition='inside', marker_cornerradius=10)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhuma atividade ativa para os filtros selecionados.")

# --- ABA 2: CONCLUÍDOS ---
with tab2:
    st.subheader("✅ Histórico de Atividades Concluídas")
    df_done = st.session_state.df[st.session_state.df['STATUS'] == 'Concluído']
    if not df_done.empty:
        st.dataframe(df_done, use_container_width=True)
    else:
        st.info("Nenhuma atividade concluída ainda.")

# --- ABA 3: CADASTRO ---
with tab3:
    st.subheader("📝 Edição e Cadastro de Dados")
    
    # GUIA DE USABILIDADE
    with st.expander("💡 Como usar a tabela?", expanded=True):
        st.markdown("""
        - **Para Editar**: Clique duas vezes em qualquer célula.
        - **Para Adicionar**: Clique no botão **"+"** no final da tabela ou no topo direito.
        - **Para Apagar**: Clique no quadradinho à esquerda da linha para selecioná-la e aperte a tecla **Delete** no seu teclado.
        - **IMPORTANTE**: Após editar, clique no botão azul **"SALVAR ALTERAÇÕES"** abaixo.
        """)

    df_ed = st.data_editor(
        st.session_state.df, num_rows="dynamic", use_container_width=True,
        column_config={
            "STATUS": st.column_config.SelectboxColumn("STATUS", options=["Pendente", "Em Andamento", "Concluído", "Atrasado"], required=True),
            "PROGRESSO": st.column_config.NumberColumn("PROGRESSO %", min_value=0, max_value=100, format="%d%%"),
            "DATA INÍCIO": st.column_config.DateColumn("INÍCIO"),
            "DATA FIM": st.column_config.DateColumn("FIM")
        },
        key="editor_v5"
    )
    
    if st.button("💾 SALVAR ALTERAÇÕES", use_container_width=True):
        st.session_state.df = df_ed
        st.success("✅ Dados salvos com sucesso!")
        st.rerun()

    st.markdown("---")
    st.subheader("📤 Importar / Exportar")
    c1, c2 = st.columns(2)
    with c1:
        f = st.file_uploader("Importar Excel", type="xlsx")
        if f:
            st.session_state.df = pd.read_excel(f)
            st.rerun()
    with c2:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.df.to_excel(w, index=False)
        st.download_button("📥 Baixar Excel", data=buf.getvalue(), file_name="pcp_dados.xlsx", use_container_width=True)

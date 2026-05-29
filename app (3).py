import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import io

# Configuração da página com tema forçado claro
st.set_page_config(
    page_title="Gantt Premium - Gestão de Atividades",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização CSS de alto nível para contraste e visual Premium
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1e293b !important; /* Texto azul marinho escuro para contraste total */
    }

    .stApp {
        background-color: #f8fafc;
    }

    /* Forçar cores escuras em todos os textos do Streamlit */
    p, span, label, h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
    }

    /* Cards de Indicadores Detalhados */
    .metric-container {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-top: 4px solid #3b82f6;
        text-align: left;
    }

    /* Estilo das Abas Premium */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        padding: 6px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        padding: 10px 20px;
        color: #475569 !important;
        transition: all 0.2s;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #2563eb !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }

    /* Botão Principal */
    .stButton>button {
        background-color: #2563eb;
        color: white !important;
        border-radius: 10px;
        border: none;
        padding: 12px;
        font-weight: 700;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }

    /* Ajuste de contraste para o editor de dados */
    [data-testid="stDataEditor"] {
        background-color: white;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE SUPORTE ---

def get_initial_data():
    return pd.DataFrame({
        'PREFIXO': ['LOTE-A1', 'LOTE-A1', 'LOTE-B2', 'LOTE-C3', 'LOTE-A1'],
        'PEÇA': ['Eixo Rotativo', 'Suporte Base', 'Engrenagem Z', 'Painel Frontal', 'Válvula 40'],
        'DATA INÍCIO': [date(2026, 5, 1), date(2026, 5, 4), date(2026, 5, 10), date(2026, 5, 15), date(2026, 5, 20)],
        'DATA FIM': [date(2026, 5, 12), date(2026, 5, 15), date(2026, 5, 25), date(2026, 6, 5), date(2026, 5, 28)],
        'AÇÃO': ['Usinagem CNC', 'Pintura Epóxi', 'Montagem Final', 'Soldagem Robotizada', 'Inspeção Final'],
        'STATUS': ['Concluído', 'Em Andamento', 'Pendente', 'Em Andamento', 'Atrasado'],
        'PROGRESSO': [100, 65, 0, 40, 15],
        'OBSERVAÇÃO': ['Qualidade aprovada.', 'Segunda demão pendente.', 'Aguardando peças.', 'Iniciado turno extra.', 'Falha no sensor.']
    })

if 'df' not in st.session_state:
    st.session_state.df = get_initial_data()

# --- LAYOUT PRINCIPAL ---

st.markdown("# 💎 Gestão de Atividades Premium")
st.markdown("### Controle de Produção e Evolução em Tempo Real")

tab_dashboard, tab_cadastro = st.tabs(["📈 Visão Geral e Gantt", "⚙️ Painel de Cadastro"])

# --- ABA 1: DASHBOARD ---
with tab_dashboard:
    # Indicadores em Cards Estilizados
    m1, m2, m3, m4, m5 = st.columns(5)
    
    with m1:
        st.markdown(f'<div class="metric-container"><b>Total</b><br><span style="font-size: 24px; font-weight: 700;">{len(st.session_state.df)}</span></div>', unsafe_allow_html=True)
    with m2:
        concluidas = len(st.session_state.df[st.session_state.df['STATUS'] == 'Concluído'])
        st.markdown(f'<div class="metric-container" style="border-top-color: #10b981;"><b>Concluídas</b><br><span style="font-size: 24px; font-weight: 700; color: #059669 !important;">{concluidas}</span></div>', unsafe_allow_html=True)
    with m3:
        andamento = len(st.session_state.df[st.session_state.df['STATUS'] == 'Em Andamento'])
        st.markdown(f'<div class="metric-container" style="border-top-color: #3b82f6;"><b>Em Andamento</b><br><span style="font-size: 24px; font-weight: 700; color: #2563eb !important;">{andamento}</span></div>', unsafe_allow_html=True)
    with m4:
        atrasadas = len(st.session_state.df[st.session_state.df['STATUS'] == 'Atrasado'])
        st.markdown(f'<div class="metric-container" style="border-top-color: #ef4444;"><b>Atrasadas</b><br><span style="font-size: 24px; font-weight: 700; color: #dc2626 !important;">{atrasadas}</span></div>', unsafe_allow_html=True)
    with m5:
        prog_medio = st.session_state.df['PROGRESSO'].mean() if not st.session_state.df.empty else 0
        st.markdown(f'<div class="metric-container" style="border-top-color: #8b5cf6;"><b>Progresso Médio</b><br><span style="font-size: 24px; font-weight: 700; color: #7c3aed !important;">{prog_medio:.1f}%</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Área de Filtros Próximos ao Gráfico
    with st.expander("🔍 Filtros Avançados", expanded=True):
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            sel_prefixo = st.multiselect("Prefixos", options=sorted(st.session_state.df['PREFIXO'].unique()), default=sorted(st.session_state.df['PREFIXO'].unique()))
        with f2:
            sel_status = st.multiselect("Status", options=["Pendente", "Em Andamento", "Concluído", "Atrasado"], default=["Pendente", "Em Andamento", "Concluído", "Atrasado"])
        with f3:
            sel_acao = st.selectbox("Ação Específica", ["Todas"] + sorted(st.session_state.df['AÇÃO'].unique().tolist()))
        with f4:
            periodo = st.date_input("Intervalo de Datas", [st.session_state.df['DATA INÍCIO'].min(), st.session_state.df['DATA FIM'].max()])

    # Aplicação dos Filtros
    df_plot = st.session_state.df.copy()
    df_plot = df_plot[df_plot['PREFIXO'].isin(sel_prefixo)]
    df_plot = df_plot[df_plot['STATUS'].isin(sel_status)]
    if sel_acao != "Todas":
        df_plot = df_plot[df_plot['AÇÃO'] == sel_acao]
    if len(periodo) == 2:
        df_plot = df_plot[(df_plot['DATA INÍCIO'] >= periodo[0]) & (df_plot['DATA FIM'] <= periodo[1])]

    # Gráfico de Gantt Premium
    if not df_plot.empty:
        # Concatenar informações para o eixo Y (Prefixo - Peça)
        df_plot['ID_COMPLETO'] = df_plot['PREFIXO'] + " - " + df_plot['PEÇA']
        
        # Paleta de Cores Corporativas Vibrantes para Contraste
        colors = {
            'Concluído': '#10b981',     # Verde Esmeralda
            'Em Andamento': '#3b82f6',  # Azul Royal
            'Pendente': '#f59e0b',      # Amarelo Âmbar
            'Atrasado': '#ef4444'       # Vermelho Intenso
        }

        fig = px.timeline(
            df_plot,
            x_start="DATA INÍCIO",
            x_end="DATA FIM",
            y="ID_COMPLETO",
            color="STATUS",
            color_discrete_map=colors,
            hover_data={"ID_COMPLETO": False, "AÇÃO": True, "PROGRESSO": True, "STATUS": True},
            text="PROGRESSO"
        )

        fig.update_yaxes(autorange="reversed", title="", tickfont=dict(color='#1e293b', size=12, family="Inter"))
        fig.update_xaxes(title="Cronograma de Execução", gridcolor='#e2e8f0', tickfont=dict(color='#1e293b'))
        
        # Linha do Dia Atual (Hoje)
        today_ts = datetime.now().timestamp() * 1000
        fig.add_vline(x=today_ts, line_width=3, line_dash="solid", line_color="#1e293b", annotation_text="HOJE", annotation_position="top left", annotation_font=dict(color="#1e293b", size=10))

        fig.update_layout(
            height=600,
            plot_bgcolor='white',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b', family="Inter"),
            margin=dict(l=10, r=10, t=50, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11)),
            showlegend=True
        )

        fig.update_traces(
            texttemplate='%{text}%', 
            textposition='inside', 
            marker_line_color='white', 
            marker_line_width=1.5,
            opacity=0.95
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.warning("⚠️ Nenhum dado corresponde aos filtros selecionados.")

# --- ABA 2: CADASTRO ---
with tab_cadastro:
    st.markdown("### 📝 Gestão da Base de Dados")
    st.write("Edite as informações abaixo. As cores e o gráfico serão atualizados automaticamente após salvar.")
    
    # Editor de Dados com Configuração de Colunas
    df_edited = st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "PREFIXO": st.column_config.TextColumn("PREFIXO", required=True),
            "PEÇA": st.column_config.TextColumn("PEÇA", required=True),
            "DATA INÍCIO": st.column_config.DateColumn("INÍCIO", format="DD/MM/YYYY"),
            "DATA FIM": st.column_config.DateColumn("FIM", format="DD/MM/YYYY"),
            "STATUS": st.column_config.SelectboxColumn("STATUS", options=["Pendente", "Em Andamento", "Concluído", "Atrasado"], required=True),
            "PROGRESSO": st.column_config.ProgressColumn("PROGRESSO", min_value=0, max_value=100, format="%d%%"),
            "AÇÃO": st.column_config.TextColumn("AÇÃO"),
            "OBSERVAÇÃO": st.column_config.TextColumn("OBSERVAÇÃO")
        },
        key="editor_premium"
    )

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("💾 SALVAR E ATUALIZAR SISTEMA", use_container_width=True):
            st.session_state.df = df_edited
            st.success("✅ Sistema atualizado com sucesso!")
            st.rerun()

    st.markdown("---")
    st.markdown("### 📤 Importação e Exportação")
    i1, i2 = st.columns(2)
    
    with i1:
        up_file = st.file_uploader("Carregar Excel (.xlsx)", type="xlsx")
        if up_file:
            try:
                new_df = pd.read_excel(up_file)
                st.session_state.df = new_df
                st.success("Dados carregados!")
                st.rerun()
            except:
                st.error("Erro ao ler arquivo. Verifique as colunas.")
                
    with i2:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.df.to_excel(writer, index=False)
        st.download_button("📥 Baixar Planilha Atual", data=buffer.getvalue(), file_name="gestao_gantt_premium.xlsx", mime="application/vnd.ms-excel", use_container_width=True)

st.markdown("<br><hr><center>Sistema de Gestão Gantt Premium v3.0 | Design Corporativo de Alta Performance</center>", unsafe_allow_html=True)

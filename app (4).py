import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import io

# Configuração da página
st.set_page_config(
    page_title="PCP - Planejamento Semanal",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS AGRESSIVO PARA FORÇAR TEMA CLARO E FONTES GRANDES
st.markdown("""
    <style>
    /* Forçar fundo branco em tudo */
    .stApp, div[data-testid="stToolbar"], .main, header, .stTabs {
        background-color: white !important;
    }

    /* Forçar texto PRETO e GRANDE em todos os elementos */
    html, body, [class*="css"], .stMarkdown, p, span, label, li, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-family: 'Arial', sans-serif !important;
    }

    /* Títulos Maiores */
    h1 { font-size: 42px !important; font-weight: 800 !important; margin-bottom: 0px !important; }
    h3 { font-size: 28px !important; font-weight: 700 !important; }

    /* Cards de Indicadores com Contraste Total */
    .metric-card {
        background-color: #ffffff !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 15px !important;
        padding: 25px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        margin-bottom: 10px !important;
    }
    
    .metric-label {
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #444444 !important;
    }
    
    .metric-value {
        font-size: 36px !important;
        font-weight: 800 !important;
        color: #000000 !important;
    }

    /* Ajuste de Filtros (Selectbox, MultiSelect, etc) */
    div[data-baseweb="select"] > div {
        background-color: #f8f9fa !important;
        border: 1px solid #cccccc !important;
    }
    
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #dddddd !important;
    }

    /* Botão de Salvar Grande */
    .stButton>button {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-size: 20px !important;
        height: 60px !important;
        border-radius: 12px !important;
        font-weight: bold !important;
    }

    /* Abas Maiores */
    .stTabs [data-baseweb="tab"] {
        font-size: 22px !important;
        height: 60px !important;
        font-weight: bold !important;
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

# --- TÍTULO ---
st.markdown("<h1>Reunião de Planejamento Semanal PCP</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #666 !important;'>Acompanhamento de Produção e Evolução</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

t1, t2 = st.tabs(["📊 DASHBOARD & GANTT", "⚙️ CADASTRO DE DADOS"])

with t1:
    # Indicadores Grandes e Visíveis
    c1, c2, c3, c4, c5 = st.columns(5)
    
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Total</div><div class="metric-value">{len(st.session_state.df)}</div></div>', unsafe_allow_html=True)
    with c2:
        val = len(st.session_state.df[st.session_state.df['STATUS'] == 'Concluído'])
        st.markdown(f'<div class="metric-card" style="border-left: 8px solid #28a745 !important;"><div class="metric-label">Concluídas</div><div class="metric-value">{val}</div></div>', unsafe_allow_html=True)
    with c3:
        val = len(st.session_state.df[st.session_state.df['STATUS'] == 'Em Andamento'])
        st.markdown(f'<div class="metric-card" style="border-left: 8px solid #007bff !important;"><div class="metric-label">Andamento</div><div class="metric-value">{val}</div></div>', unsafe_allow_html=True)
    with c4:
        val = len(st.session_state.df[st.session_state.df['STATUS'] == 'Atrasado'])
        st.markdown(f'<div class="metric-card" style="border-left: 8px solid #dc3545 !important;"><div class="metric-label">Atrasadas</div><div class="metric-value">{val}</div></div>', unsafe_allow_html=True)
    with c5:
        val = st.session_state.df['PROGRESSO'].mean() if not st.session_state.df.empty else 0
        st.markdown(f'<div class="metric-card" style="border-left: 8px solid #6f42c1 !important;"><div class="metric-label">Progresso</div><div class="metric-value">{val:.0f}%</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filtros Próximos ao Gráfico
    with st.expander("🔍 FILTROS DE VISUALIZAÇÃO", expanded=True):
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            sel_pref = st.multiselect("Prefixos", options=sorted(st.session_state.df['PREFIXO'].unique()), default=sorted(st.session_state.df['PREFIXO'].unique()))
        with f2:
            sel_stat = st.multiselect("Status", options=["Pendente", "Em Andamento", "Concluído", "Atrasado"], default=["Pendente", "Em Andamento", "Concluído", "Atrasado"])
        with f3:
            sel_ac = st.selectbox("Ação", ["Todas"] + sorted(st.session_state.df['AÇÃO'].unique().tolist()))
        with f4:
            per = st.date_input("Período", [st.session_state.df['DATA INÍCIO'].min(), st.session_state.df['DATA FIM'].max()])

    # Filtro
    df_p = st.session_state.df.copy()
    df_p = df_p[df_p['PREFIXO'].isin(sel_pref)]
    df_p = df_p[df_p['STATUS'].isin(sel_stat)]
    if sel_ac != "Todas": df_p = df_p[df_p['AÇÃO'] == sel_ac]
    if len(per) == 2: df_p = df_p[(df_p['DATA INÍCIO'] >= per[0]) & (df_p['DATA FIM'] <= per[1])]

    # Gráfico de Gantt
    if not df_p.empty:
        df_p['ID'] = df_p['PREFIXO'] + " - " + df_p['PEÇA']
        colors = {'Concluído': '#28a745', 'Em Andamento': '#007bff', 'Pendente': '#ffc107', 'Atrasado': '#dc3545'}

        fig = px.timeline(
            df_p, x_start="DATA INÍCIO", x_end="DATA FIM", y="ID", color="STATUS",
            color_discrete_map=colors, text="PROGRESSO",
            hover_data=["AÇÃO", "PROGRESSO", "STATUS"]
        )

        fig.update_yaxes(autorange="reversed", title="", tickfont=dict(size=14, color='black', family="Arial Black"))
        fig.update_xaxes(title="Cronograma", tickfont=dict(size=12, color='black'))
        
        # Hoje
        fig.add_vline(x=datetime.now().timestamp()*1000, line_width=4, line_color="black", annotation_text="HOJE")

        fig.update_layout(
            height=600, plot_bgcolor='white', paper_bgcolor='white',
            font=dict(color='black', size=14),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        fig.update_traces(texttemplate='%{text}%', textposition='inside', marker_line_color='white', marker_line_width=2)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Sem dados para exibir.")

with t2:
    st.markdown("<h3>📝 Edição da Tabela</h3>", unsafe_allow_html=True)
    df_ed = st.data_editor(
        st.session_state.df, num_rows="dynamic", use_container_width=True,
        column_config={
            "STATUS": st.column_config.SelectboxColumn("STATUS", options=["Pendente", "Em Andamento", "Concluído", "Atrasado"], required=True),
            "PROGRESSO": st.column_config.NumberColumn("PROGRESSO %", min_value=0, max_value=100, format="%d%%"),
            "DATA INÍCIO": st.column_config.DateColumn("INÍCIO"),
            "DATA FIM": st.column_config.DateColumn("FIM")
        }
    )
    if st.button("💾 SALVAR ALTERAÇÕES E ATUALIZAR GRÁFICO"):
        st.session_state.df = df_ed
        st.success("Dados salvos!")
        st.rerun()

    st.markdown("---")
    st.markdown("<h3>📤 Importar / Exportar</h3>", unsafe_allow_html=True)
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        f = st.file_uploader("Subir Excel", type="xlsx")
        if f:
            st.session_state.df = pd.read_excel(f)
            st.rerun()
    with col_i2:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.df.to_excel(w, index=False)
        st.download_button("📥 Baixar Excel", data=buf.getvalue(), file_name="pcp_planejamento.xlsx")

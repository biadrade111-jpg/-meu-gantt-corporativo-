import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date
import io
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="PCP Moderno - Gestão de Atividades",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS PARA DESIGN MODERNO E CORPORATIVO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Fundo Branco Limpo */
    .stApp, [data-testid="stHeader"], [data-testid="stSidebar"], .main {
        background-color: #f8fafc !important;
    }

    /* Texto Preto Corporativo */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #1e293b !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Cartões com Sombra Suave */
    [data-testid="stMetricContainer"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
    }

    /* Botões Modernos */
    .stButton>button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        height: 50px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stButton>button:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    /* Selectbox e Inputs Modernos */
    .stSelectbox, .stMultiSelect, .stDateInput {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-baseweb="select"] {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
    }

    [data-baseweb="input"] {
        border-radius: 10px !important;
        border: 2px solid #e2e8f0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Abas Modernas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        padding: 0;
        border-radius: 0;
        border-bottom: 2px solid #e2e8f0;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        color: #64748b !important;
        font-weight: 600 !important;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #2563eb !important;
        border-bottom: 3px solid #2563eb !important;
    }

    /* Expander Moderno */
    .streamlit-expanderHeader {
        background-color: #f1f5f9 !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        padding: 16px !important;
        font-weight: 600 !important;
    }

    /* Data Editor (Tabela) */
    [data-testid="stDataEditor"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    }

    /* Métrica Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
        text-align: center;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.1) !important;
        transform: translateY(-4px);
    }

    /* Cores de Status */
    .status-concluido { color: #10b981 !important; }
    .status-andamento { color: #3b82f6 !important; }
    .status-pendente { color: #f59e0b !important; }
    .status-atrasado { color: #ef4444 !important; }

    /* Divisor */
    hr {
        border: none !important;
        border-top: 2px solid #e2e8f0 !important;
        margin: 24px 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS ---
def get_data():
    return pd.DataFrame({
        'PREFIXO': ['LOTE-01', 'LOTE-01', 'LOTE-02', 'LOTE-03', 'LOTE-01', 'LOTE-04'],
        'PEÇA': ['Suporte Base', 'Suporte Base', 'Engrenagem Z', 'Painel Frontal', 'Válvula 40', 'Eixo Principal'],
        'AÇÃO': ['Usinagem', 'Pintura', 'Furação', 'Montagem', 'Inspeção', 'Soldagem'],
        'DATA INÍCIO': [date(2026, 5, 1), date(2026, 5, 4), date(2026, 5, 10), date(2026, 5, 15), date(2026, 5, 20), date(2026, 5, 22)],
        'DATA FIM': [date(2026, 5, 12), date(2026, 5, 15), date(2026, 5, 25), date(2026, 6, 5), date(2026, 5, 28), date(2026, 6, 10)],
        'STATUS': ['Concluído', 'Em Andamento', 'Pendente', 'Em Andamento', 'Atrasado', 'Pendente'],
        'PROGRESSO': [100, 65, 0, 40, 15, 0],
        'OBSERVAÇÃO': ['OK', 'Secagem', 'Peças', 'Turno 2', 'Fornecedor', 'Agendado'],
        'SEGMENTO': ['Estrutura', 'Acabamento', 'Usinagem', 'Montagem', 'Qualidade', 'Soldagem'],
        'RESPONSÁVEL': ['João Silva', 'Maria Santos', 'Carlos Costa', 'Pedro Oliveira', 'Ana Ferreira', 'Roberto Gomes']
    })

if 'df' not in st.session_state:
    st.session_state.df = get_data()

# --- HEADER ---
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("### 🗓️ PCP Moderno")
with col2:
    st.markdown("### Gestão de Atividades - Gráfico de Gantt")

st.markdown("---")

# --- ABAS PRINCIPAIS ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard & Gantt", "✅ Atividades Concluídas", "⚙️ Cadastro e Edição"])

# --- ABA 1: DASHBOARD ---
with tab1:
    # KPIs
    st.subheader("📈 Indicadores de Desempenho")
    
    m1, m2, m3, m4, m5 = st.columns(5)
    
    total = len(st.session_state.df)
    concluidas = len(st.session_state.df[st.session_state.df['STATUS'] == 'Concluído'])
    em_andamento = len(st.session_state.df[st.session_state.df['STATUS'] == 'Em Andamento'])
    atrasadas = len(st.session_state.df[st.session_state.df['STATUS'] == 'Atrasado'])
    progresso_medio = st.session_state.df['PROGRESSO'].mean()
    
    with m1:
        st.metric("📋 Total", total, "100% do total")
    with m2:
        st.metric("✅ Concluídas", concluidas, f"{(concluidas/total*100):.0f}%")
    with m3:
        st.metric("⏳ Em Andamento", em_andamento, f"{(em_andamento/total*100):.0f}%")
    with m4:
        st.metric("⚠️ Atrasadas", atrasadas, f"{(atrasadas/total*100):.0f}%")
    with m5:
        st.metric("📊 Progresso Médio", f"{progresso_medio:.1f}%", "Média geral")

    st.markdown("---")

    # Filtros
    st.subheader("🔍 Filtros de Visualização")
    
    with st.expander("Clique para expandir/recolher filtros", expanded=True):
        f1, f2, f3, f4, f5, f6 = st.columns(6)
        
        with f1:
            s_pref = st.multiselect(
                "Prefixo",
                options=sorted(st.session_state.df['PREFIXO'].unique()),
                default=sorted(st.session_state.df['PREFIXO'].unique()),
                key="prefixo_filter"
            )
        
        with f2:
            s_stat = st.multiselect(
                "Status",
                options=["Pendente", "Em Andamento", "Atrasado", "Concluído"],
                default=["Pendente", "Em Andamento", "Atrasado", "Concluído"],
                key="status_filter"
            )
        
        with f3:
            s_acao = st.multiselect(
                "Ação",
                options=sorted(st.session_state.df['AÇÃO'].unique()),
                default=sorted(st.session_state.df['AÇÃO'].unique()),
                key="acao_filter"
            )
        
        with f4:
            s_segmento = st.multiselect(
                "Segmento",
                options=sorted(st.session_state.df['SEGMENTO'].unique()),
                default=sorted(st.session_state.df['SEGMENTO'].unique()),
                key="segmento_filter"
            )
        
        with f5:
            s_responsavel = st.multiselect(
                "Responsável",
                options=sorted(st.session_state.df['RESPONSÁVEL'].unique()),
                default=sorted(st.session_state.df['RESPONSÁVEL'].unique()),
                key="responsavel_filter"
            )
        
        with f6:
            per = st.date_input(
                "Período",
                value=[st.session_state.df['DATA INÍCIO'].min(), st.session_state.df['DATA FIM'].max()],
                key="periodo_filter"
            )

    # Aplicar filtros
    df_filtrado = st.session_state.df[
        (st.session_state.df['PREFIXO'].isin(s_pref)) &
        (st.session_state.df['STATUS'].isin(s_stat)) &
        (st.session_state.df['AÇÃO'].isin(s_acao)) &
        (st.session_state.df['SEGMENTO'].isin(s_segmento)) &
        (st.session_state.df['RESPONSÁVEL'].isin(s_responsavel)) &
        (st.session_state.df['DATA INÍCIO'] >= per[0]) &
        (st.session_state.df['DATA FIM'] <= per[1])
    ].copy()

    st.markdown("---")

    # Gráfico de Gantt Moderno
    st.subheader("📅 Cronograma de Atividades (Gráfico de Gantt)")
    
    if not df_filtrado.empty:
        # Cores por status
        cores_status = {
            'Concluído': '#10b981',
            'Em Andamento': '#3b82f6',
            'Pendente': '#f59e0b',
            'Atrasado': '#ef4444'
        }
        
        # Preparar dados para Gantt
        df_gantt = df_filtrado.copy()
        df_gantt['ID'] = df_gantt['PREFIXO'] + " - " + df_gantt['PEÇA'] + " (" + df_gantt['AÇÃO'] + ")"
        df_gantt['Cor'] = df_gantt['STATUS'].map(cores_status)
        
        # Criar figura Gantt
        fig = go.Figure()
        
        for idx, row in df_gantt.iterrows():
            fig.add_trace(go.Bar(
                y=[row['ID']],
                x=[row['DATA FIM'] - row['DATA INÍCIO']],
                base=[row['DATA INÍCIO']],
                orientation='h',
                marker=dict(
                    color=row['Cor'],
                    line=dict(color='white', width=2),
                    opacity=0.9
                ),
                text=f"{row['PROGRESSO']}%",
                textposition='inside',
                textfont=dict(color='white', size=12, family='Plus Jakarta Sans'),
                hovertemplate=f"<b>{row['ID']}</b><br>" +
                             f"Início: {row['DATA INÍCIO']}<br>" +
                             f"Fim: {row['DATA FIM']}<br>" +
                             f"Status: {row['STATUS']}<br>" +
                             f"Progresso: {row['PROGRESSO']}%<br>" +
                             f"Responsável: {row['RESPONSÁVEL']}<extra></extra>",
                name=row['STATUS'],
                showlegend=False
            ))
        
        # Adicionar linha de hoje
        hoje = pd.Timestamp(datetime.now().date())
        fig.add_vline(
            x=hoje,
            line_width=3,
            line_color="#1e293b",
            line_dash="dash",
            annotation_text="HOJE",
            annotation_position="top right",
            annotation_font=dict(size=12, color="#1e293b", family='Plus Jakarta Sans')
        )
        
        # Configurar layout
        fig.update_layout(
            title={
                'text': "Cronograma de Atividades (Gráfico de Gantt)",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': '#1e293b', 'family': 'Plus Jakarta Sans'}
            },
            xaxis=dict(
                type='date',
                tickformat='%d/%b\n(%a)',
                tickfont=dict(size=11, family='Plus Jakarta Sans'),
                gridcolor='#e2e8f0',
                showgrid=True,
                zeroline=False,
                side='bottom'
            ),
            yaxis=dict(
                tickfont=dict(size=11, family='Plus Jakarta Sans'),
                autorange='reversed',
                showgrid=False
            ),
            plot_bgcolor='#ffffff',
            paper_bgcolor='#f8fafc',
            margin=dict(l=250, r=50, t=100, b=80),
            height=max(400, len(df_gantt) * 50),
            hovermode='closest',
            font=dict(family='Plus Jakarta Sans', size=11, color='#1e293b'),
            showlegend=False
        )
        
        # Adicionar grid vertical para melhor leitura
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Legenda de Status
        st.markdown("#### Legenda de Status")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<span style="color: #10b981; font-weight: bold;">● Concluído</span>', unsafe_allow_html=True)
        with col2:
            st.markdown('<span style="color: #3b82f6; font-weight: bold;">● Em Andamento</span>', unsafe_allow_html=True)
        with col3:
            st.markdown('<span style="color: #f59e0b; font-weight: bold;">● Pendente</span>', unsafe_allow_html=True)
        with col4:
            st.markdown('<span style="color: #ef4444; font-weight: bold;">● Atrasado</span>', unsafe_allow_html=True)
        
    else:
        st.info("ℹ️ Nenhuma atividade encontrada com os filtros selecionados.")

# --- ABA 2: CONCLUÍDOS ---
with tab2:
    st.subheader("✅ Histórico de Atividades Concluídas")
    df_done = st.session_state.df[st.session_state.df['STATUS'] == 'Concluído']
    
    if not df_done.empty:
        st.dataframe(df_done, use_container_width=True, hide_index=True)
        st.metric("Total Concluídas", len(df_done))
    else:
        st.info("ℹ️ Nenhuma atividade concluída ainda.")

# --- ABA 3: CADASTRO ---
with tab3:
    st.subheader("📝 Edição e Cadastro de Dados")
    
    # Guia de Usabilidade
    with st.expander("💡 Como usar a tabela?", expanded=True):
        st.markdown("""
        - **Para Editar**: Clique duas vezes em qualquer célula.
        - **Para Adicionar**: Clique no botão **"+"** no final da tabela ou no topo direito.
        - **Para Apagar**: Clique no quadradinho à esquerda da linha para selecioná-la e aperte a tecla **Delete** no seu teclado.
        - **IMPORTANTE**: Após editar, clique no botão azul **"SALVAR ALTERAÇÕES"** abaixo.
        """)

    # Data Editor
    df_ed = st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "STATUS": st.column_config.SelectboxColumn(
                "STATUS",
                options=["Pendente", "Em Andamento", "Concluído", "Atrasado"],
                required=True
            ),
            "PROGRESSO": st.column_config.NumberColumn(
                "PROGRESSO %",
                min_value=0,
                max_value=100,
                format="%d%%"
            ),
            "DATA INÍCIO": st.column_config.DateColumn("INÍCIO"),
            "DATA FIM": st.column_config.DateColumn("FIM")
        },
        key="editor_v5"
    )
    
    # Botão Salvar
    if st.button("💾 SALVAR ALTERAÇÕES", use_container_width=True):
        st.session_state.df = df_ed
        st.success("✅ Dados salvos com sucesso!")
        st.rerun()

    st.markdown("---")
    st.subheader("📤 Importar / Exportar")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### 📥 Importar Excel")
        f = st.file_uploader("Selecione um arquivo CSV ou XLSX", type=["xlsx", "csv"])
        if f:
            try:
                if f.name.endswith('.csv'):
                    st.session_state.df = pd.read_csv(f)
                else:
                    st.session_state.df = pd.read_excel(f)
                st.success("✅ Arquivo importado com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao importar: {str(e)}")
    
    with c2:
        st.markdown("#### 📤 Exportar Excel")
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as w:
            st.session_state.df.to_excel(w, index=False)
        
        st.download_button(
            label="📥 Baixar Excel",
            data=buf.getvalue(),
            file_name=f"pcp_dados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 12px; margin-top: 20px;">
    <p>🗓️ <b>PCP Moderno</b> - Sistema de Gestão de Atividades | Última atualização: 25/05/2026 10:30</p>
    <p>💡 Dica: Use os filtros para encontrar rapidamente o que você precisa!</p>
</div>
""", unsafe_allow_html=True)

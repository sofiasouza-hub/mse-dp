import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar
from supabase import create_client, Client

# Configuração da Página
st.set_page_config(page_title="MSE | DP", page_icon="🔴", layout="wide")

# Estilização CSS para forçar o tema claro e contraste correto
st.markdown("""
    <style>
        /* Forçar fundo claro na aplicação inteira */
        .stApp, .main, [data-testid="stAppViewContainer"] {
            background-color: #F4F6F8 !important;
            color: #111827 !important;
        }
        
        /* Garantir cor visível nos títulos e textos */
        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: #111827 !important;
        }

        /* Topbar */
        .topbar {
            background-color: #1E293B !important;
            padding: 14px 24px;
            border-radius: 8px;
            color: white !important;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .topbar * { color: white !important; }
        .logo-text { font-size: 26px; font-weight: bold; color: #EF4444 !important; }
        .dept-text { font-size: 22px; font-weight: bold; color: #FFFFFF !important; margin-left: 8px; }
        
        /* Estilo dos Cards em Fundo Branco */
        .css-card {
            background-color: #FFFFFF !important;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            border: 1px solid #E5E7EB;
        }

        .card-prox-lembrete {
            background-color: #FEF2F2 !important;
            border: 1px solid #FECACA !important;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .time-highlight {
            font-size: 40px !important;
            font-weight: 800 !important;
            color: #DC2626 !important;
            margin: 8px 0;
        }
        
        /* Estilização dos Inputs e Botões */
        .stTextInput input, .stSelectbox select, .stDateInput input, .stTimeInput input {
            background-color: #FFFFFF !important;
            color: #111827 !important;
            border: 1px solid #D1D5DB !important;
            border-radius: 6px !important;
        }
        
        .stButton>button {
            background-color: #DC2626 !important;
            color: #FFFFFF !important;
            border-radius: 6px !important;
            font-weight: bold !important;
            border: none !important;
            padding: 8px 16px !important;
        }
        .stButton>button:hover { background-color: #B91C1C !important; }
        .stButton>button * { color: #FFFFFF !important; }

        /* Abas superiores */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #FFFFFF !important;
            border-radius: 8px 8px 0 0 !important;
            padding: 10px 20px !important;
            font-weight: bold !important;
            color: #4B5563 !important;
            border: 1px solid #E5E7EB !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #DC2626 !important;
            color: #FFFFFF !important;
            border: none !important;
        }
        .stTabs [aria-selected="true"] * {
            color: #FFFFFF !important;
        }

        /* Calendário Customizado */
        .cal-header {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 12px;
            color: #111827 !important;
        }
        .cal-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 6px;
            text-align: center;
            font-size: 13px;
        }
        .cal-day-name { font-weight: bold; color: #6B7280 !important; padding-bottom: 4px; }
        .cal-day {
            padding: 6px 0;
            border-radius: 50%;
            color: #1F2937 !important;
        }
        .cal-day-active {
            background-color: #DC2626 !important;
            color: #FFFFFF !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Conexão Supabase
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# Lista de equipe
@st.cache_data(ttl=5)
def get_colaboradores():
    try:
        res = supabase.table("colaboradores").select("nome").order("nome").execute()
        nomes = [item['nome'] for item in res.data] if res.data else []
        if not nomes:
            nomes = ['ANY', 'BRUNA', 'FERNANDA', 'ISAAC', 'MARIA', 'NATALIA', 'SOFIA']
        return nomes
    except Exception:
        return ['ANY', 'BRUNA', 'FERNANDA', 'ISAAC', 'MARIA', 'NATALIA', 'SOFIA']

lista_equipe = get_colaboradores()

# --- TOPBAR ---
st.markdown("""
    <div class="topbar">
        <div>
            <span class="logo-text">MSE</span>
            <span class="dept-text">| DP</span>
        </div>
        <div>
            <span>🟢 Nuvem Conectada</span>
        </div>
    </div>
""", unsafe_allow_html=True)

col_top1, col_top2 = st.columns([3, 1])
with col_top2:
    idx_padrao = lista_equipe.index("SOFIA") if "SOFIA" in lista_equipe else 0
    usuario_ativo = st.selectbox("👤 Usuário:", options=lista_equipe, index=idx_padrao)

if not usuario_ativo:
    usuario_ativo = "SOFIA"

# --- NAVEGAÇÃO POR ABAS ---
aba1, aba2, aba3, aba4 = st.tabs(["🔔 Meus Lembretes", "📅 Calendário Coletivo", "📋 Mural da Equipe", "⚙️ Gerenciar Equipe"])

# --- ABA 1: MEUS LEMBRETES ---
with aba1:
    col_principal, col_lateral = st.columns([2.2, 1])
    
    with col_principal:
        st.subheader("💬 O que você precisa lembrar?")
        
        c_input, c_data, c_hora = st.columns([2, 1, 1])
        with c_input:
            texto_lembrete = st.text_input("Lembrete", placeholder="Ex: Dia 08/02 às 09:00, subir e-mail", label_visibility="collapsed")
        with c_data:
            data_lembrete = st.date_input("Data", value=date.today(), label_visibility="collapsed")
        with c_hora:
            hora_lembrete = st.time_input("Horário", label_visibility="collapsed")
            
        col_check, col_btn = st.columns([2, 1])
        with col_check:
            recorrente = st.checkbox("Repetir este lembrete todo mês")
        with col_btn:
            btn_agendar = st.button("🗓️ Agendar Lembrete →", use_container_width=True)
            
        if btn_agendar:
            if texto_lembrete:
                dt_completa = datetime.combine(data_lembrete, hora_lembrete).isoformat()
                supabase.table("lembretes").insert({
                    "usuario": usuario_ativo,
                    "conteudo": texto_lembrete,
                    "data_hora": dt_completa,
                    "recorrente_mensal": recorrente

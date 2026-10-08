import streamlit as st
import pandas as pd
from datetime import datetime, date
from html import escape
import calendar
from dateutil.relativedelta import relativedelta
from supabase import create_client, Client

# Configuração da página
st.set_page_config(
    page_title="MSE | DP",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Estilização CSS limpa e sem dependências complexas
st.markdown("""
<style>
.stApp { background: #f3f4f6; color: #1e293b; }
.block-container { max-width: 1240px; padding: 16px 24px 28px 24px; }
#MainMenu, footer, header { visibility: hidden; }

/* TOPBAR */
.topbar {
    height: 58px; background: #1e293b; border-radius: 6px; padding: 0 18px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 2px 6px rgba(15, 23, 42, .12); margin-bottom: 12px;
}
.brand { display: flex; align-items: center; gap: 10px; }
.brand-mse { color: #ef233c; font-size: 27px; font-weight: 900; letter-spacing: -1.5px; }
.brand-divider { color: #64748b; font-size: 21px; }
.brand-dp { color: white; font-size: 16px; font-weight: 700; }
.top-status { display: flex; align-items: center; gap: 20px; color: #e2e8f0; font-size: 12px; }
.connected { color: #4ade80; font-weight: 600; }

/* CARDS BRANCOS */
.card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 7px; padding: 15px 18px; margin-bottom: 12px; }
.card-title { color: #1e3a5f; font-size: 15px; font-weight: 750; margin-bottom: 11px; }

/* TABELA E BADGES */
.reminder-table { width: 100%; border-collapse: collapse; font-size: 11px; }
.reminder-table th { background: #f1f5f9; color: #64748b; text-align: left; padding: 8px 9px; font-size: 10px; }
.reminder-table td { color: #334155; padding: 9px; border-bottom: 1px solid #edf2f7; }
.badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 9px; font-weight: 750; }
.badge-pendente { background: #fef3c7; color: #d97706; }
.badge-concluido { background: #d1fae5; color: #059669; }

/* CALENDÁRIO LATERAL */
.calendar-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 7px; padding: 15px 16px; }
.calendar-head { display: flex; justify-content: space-between; align-items: center; color: #1e3a5f; font-size: 14px; font-weight: 750; margin-bottom: 13px; }
.cal-grid-clickable { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; text-align: center; }
.cal-weekday-clickable { color: #94a3b8; font-size: 9px; font-weight: 700; padding-bottom: 5px; }
.cal-empty { min-height: 31px; }
.cal-link { display: flex; flex-direction: column; align-items: center; justify-content: flex-start; min-height: 31px; color: #475569 !important; text-decoration: none !important; font-size: 10px; }
.cal-number { width: 24px; height: 24px; line-height: 24px; border-radius: 50%; }
.cal-number.today { background: #dc2638; color: #ffffff; font-weight: 800; }
.cal-number.selected { outline: 2px solid #dc2638; outline-offset: 1px; font-weight: 800; }
.cal-dot-red { width: 4px; height: 4px; background: #dc2638; border-radius: 50%; margin-top: 1px; }
.calendar-selected { margin-top: 10px; background: #f8fafc; border: 1px solid #e5e7eb; border-left: 3px solid #dc2638; border-radius: 6px; padding: 10px 11px; }
.soft-divider { height: 1px; background: #edf2f7; margin: 8px 0 12px; }
</style>
""", unsafe_allow_html=True)

# Supabase Client
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro de conexão com o Supabase: {e}")
        return None

supabase = init_supabase()

# Dados de Colaboradores
@st.cache_data(ttl=5)
def get_colaboradores():
    if not supabase:
        return ["ANY", "BRUNA", "FERNANDA", "ISAAC", "MARIA", "NATALIA", "SOFIA"]
    try:
        res = supabase.table("colaboradores").select("nome").order("nome").execute()
        nomes = [item["nome"] for item in res.data] if res.data else []
        return nomes if nomes else ["ANY", "BRUNA", "FERNANDA", "ISAAC", "MARIA", "NATALIA", "SOFIA"]
    except Exception:
        return ["ANY", "BRUNA", "FERNANDA", "ISAAC", "MARIA", "NATALIA", "SOFIA"]

lista_equipe = get_colaboradores()

# Header / Topbar
st.markdown("""
<div class="topbar">
    <div class="brand">
        <span class="brand-mse">MSE</span>
        <span class="brand-divider">|</span>
        <span class="brand-dp">DP</span>
    </div>
    <div class="top-status">
        <span class="connected">● Nuvem Conectada</span>
        <span>|</span>
        <span>👤 Usuário: Sofia</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Seleção de usuário ativo
idx_padrao = lista_equipe.index("SOFIA") if "SOFIA" in lista_equipe else 0
col_user, _ = st.columns([0.55, 4.45])
with col_user:
    usuario_ativo = st.selectbox("Usuário ativo", options=lista_equipe, index=idx_padrao, label_visibility="

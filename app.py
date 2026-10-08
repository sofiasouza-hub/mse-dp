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
            gap: 12

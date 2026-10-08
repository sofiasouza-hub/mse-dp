import streamlit as st
import pandas as pd
from datetime import datetime, date
from html import escape
import calendar
import textwrap
from dateutil.relativedelta import relativedelta
from supabase import create_client, Client

# ============================================================
# CONFIGURAÇÃO
# ============================================================
st.set_page_config(
    page_title="MSE | DP",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS — VISUAL DA REFERÊNCIA (COM FIX DEFINITIVO DE CARD BRANCO)
# ============================================================
st.markdown(textwrap.dedent("""
<style>
/* ---------- BASE ---------- */
.stApp {
    background: #f3f4f6;
    color: #1e293b;
}

.block-container {
    max-width: 1240px;
    padding: 16px 24px 28px 24px;
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* Remove espaços exagerados do Streamlit */
div[data-testid="stVerticalBlock"] {
    gap: 0.55rem;
}

/* ---------- TOPBAR ---------- */
.topbar {
    height: 58px;
    background: #1e293b;
    border-radius: 6px;
    padding: 0 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 6px rgba(15, 23, 42, .12);
    margin-bottom: 12px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.brand-mse {
    color: #ef233c;
    font-size: 27px;
    font-weight: 900;
    letter-spacing: -1.5px;
}

.brand-divider {
    color: #64748b;
    font-size: 21px;
}

.brand-dp {
    color: white;
    font-size: 16px;
    font-weight: 700;
}

.top-status {
    display: flex;
    align-items: center;
    gap: 20px;
    color: #e2e8f0;
    font-size: 12px;
}

.connected {
    color: #4ade80;
    font-weight: 600;
}

/* ---------- MENU PRINCIPAL ---------- */
div[role="radiogroup"] {
    gap: 7px !important;
    background: transparent !important;
    flex-wrap: wrap !important;
}

div[role="radiogroup"] > label {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 5px !important;
    min-height: 38px !important;
    padding: 0 14px !important;
    box-shadow: 0 1px 2px rgba(15,23,42,.04);
    color: #475569 !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    cursor: pointer !important;
}

div[role="radiogroup"] > label:hover {
    border-color: #dc2638 !important;
    color: #dc2638 !important;
}

div[role="radiogroup"] > label:has(input:checked) {
    background: #ffffff !important;
    border: 2px solid #dc2638 !important;
    color: #dc2638 !important;
    box-shadow: 0 1px 4px rgba(220,38,56,.12);
}

div[role="radiogroup"] > label input {
    display: none !important;
}

div[role="radiogroup"] > label > div:first-child { display: none !important; }

/* ---------- CARDS ---------- */
.card {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 7px !important;
    padding: 18px 20px !important;
    box-shadow: 0 1px 4px rgba(15,23,42,.045) !important;
    margin-bottom: 12px !important;
}

.card-title {
    color: #1e3a5f;
    font-size: 15px;
    font-weight: 750;
    margin-bottom: 11px;
}

/* ---------- ESTRUTURA DO MURAL (FORÇA BRANCO ABSOLUTO) ---------- */
.st-key-mural_card {
    background-color: #ffffff !important;
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 7px !important;
    padding: 18px 20px !important;
    box-shadow: 0 1px 4px rgba(15,23,42,.045) !important;
}

.st-key-mural_card div[data-testid="stVerticalBlock"] {
    background-color: #ffffff !important;
}

/* ---------- SELECTBOX DO FILTRO ---------- */
div[data-testid="stSelectbox"] label p {
    color: #475569 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #ffffff !important;
    border: 1px solid #dbe3ec !important;
    border-radius: 5px !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] * {
    background-color: #ffffff !important;
    color: #1e293b !important;
}

/* ---------- NOVO LEMBRETE ---------- */
.st-key-reminder_form {
    background: #ffffff !important;
    border: 1px solid #e4e9ef !important;
    border-radius: 6px !important;
    padding: 13px 16px 12px 16px !important;
    box-shadow: 0 1px 4px rgba(15,23,42,.045) !important;
    margin-bottom: 12px !important;
}

.st-key-reminder_form .reminder-form-title {
    display: flex;
    align-items: center;
    gap: 7px;
    color: #17395f;
    font-size: 14px;
    font-weight: 800;
    margin: 0 0 10px 0;
}

.st-key-reminder_form div[data-testid="stTextInput"] input,
.st-key-reminder_form div[data-testid="stDateInput"] input,
.st-key-reminder_form div[data-testid="stTimeInput"] input {
    height: 38px !important;
    min-height: 38px !important;
    border: 1px solid #dce5ee !important;
    border-radius: 5px !important;
    padding: 0 12px !important;
    color: #334155 !important;
    background: #ffffff !important;
}

.st-key-reminder_form div[data-testid="stCheckbox"] label {
    color: #526b86 !important;
    font-size: 11px !important;
}

/* ---------- INPUT

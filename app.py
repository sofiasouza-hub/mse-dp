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
# CSS — VISUAL DA REFERÊNCIA
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

/* ---------- USUÁRIO ---------- */
.user-row {
    margin-top: -1px;
    margin-bottom: 9px;
}

.user-label {
    color: #64748b;
    font-size: 11px;
    margin-bottom: -7px;
}

/* ---------- MENU PRINCIPAL (AJUSTADO PARA ESCONDER A BOLINHA COMPLETAMENTE) ---------- */
div[data-testid="stRadio"] > div[role="radiogroup"],
div[role="radiogroup"] {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
    align-items: center !important;
    margin: 8px 0 16px 0 !important;
    background: transparent !important;
}

div[data-testid="stRadio"] > div[role="radiogroup"] > label,
div[role="radiogroup"] > label {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: auto !important;
    min-height: 36px !important;
    padding: 0 16px !important;
    margin: 0 !important;
    border: 1px solid #d9dee7 !important;
    border-radius: 6px !important;
    background: #ffffff !important;
    color: #334155 !important;
    cursor: pointer !important;
    box-sizing: border-box !important;
    transition: all .15s ease !important;
    box-shadow: 0 1px 2px rgba(15,23,42,.04) !important;
}

/* Esconde todas as variações de bolinha/rádio nativas do Streamlit */
div[role="radiogroup"] > label > div:first-child,
div[role="radiogroup"] input[type="radio"],
div[data-testid="stRadioButtonCustomIcon"] {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* O texto inteiro fica dentro do quadradinho */
div[role="radiogroup"] > label p,
div[role="radiogroup"] > label span {
    color: inherit !important;
    margin: 0 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* Passando o mouse */
div[role="radiogroup"] > label:hover {
    border-color: #dc2638 !important;
    color: #dc2638 !important;
    background: #ffffff !important;
}

/* ABA SELECIONADA: Fundo vermelho com texto branco */
div[role="radiogroup"] > label:has(input:checked),
div[role="radiogroup"] > label[aria-checked="true"] {
    border: 1px solid #dc2638 !important;
    border-radius: 6px !important;
    background: #dc2638 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 5px rgba(220,38,56,.2) !important;
}

div[role="radiogroup"] > label:has(input:checked) p,
div[role="radiogroup"] > label[aria-checked="true"] p,
div[role="radiogroup"] > label:has(input:checked) span,
div[role="radiogroup"] > label[aria-checked="true"] span {
    color: #ffffff !important;
}

/* ---------- CARDS ---------- */
.card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 7px;
    padding: 15px 18px;
    box-shadow: 0 1px 4px rgba(15,23,42,.045);
    margin-bottom: 12px;
}

.card-title {
    color: #1e3a5f;
    font-size: 15px;
    font-weight: 750;
    margin-bottom: 11px;
}

.card-title-red {
    color: #dc2638;
    font-size: 14px;
    font-weight: 750;
}

/* ---------- NOVO LEMBRETE — VISUAL DA REFERÊNCIA ---------- */
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

.st-key-reminder_form .reminder-form-title-icon {
    font-size: 15px;
    line-height: 1;
    filter: saturate(.65);
}

.st-key-reminder_form div[data-testid="stTextInput"] {
    margin-bottom: 9px !important;
}

.st-key-reminder_form div[data-testid="stTextInput"] input {
    height: 38px !important;
    min-height: 38px !important;
    border: 1px solid #dce5ee !important;
    border-radius: 5px !important;
    padding: 0 12px !important;
    color: #334155 !important;
    font-size: 11px !important;
    background: #ffffff !important;
}

.st-key-reminder_form div[data-testid="stTextInput"] input::placeholder {
    color: #9aaec3 !important;
}

/* Data e hora ficam visíveis em duas caixas separadas. */
.st-key-reminder_form div[data-testid="stDateInput"],
.st-key-reminder_form div[data-testid="stTimeInput"] {
    display: block !important;
    margin-bottom: 9px !important;
}

.st-key-reminder_form div[data-testid="stDateInput"] input,
.st-key-reminder_form div[data-testid="stTimeInput"] input {
    height: 38px !important;
    min-height: 38px !important;
    border: 1px solid #dce5ee !important;
    border-radius: 5px !important;
    padding: 0 12px !important;
    color: #334155 !important;
    font-size: 11px !important;
    background: #ffffff !important;
}

/* Mantém a linha inferior compacta. */
.st-key-reminder_form div[data-testid="stCheckbox"] {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

.st-key-reminder_form div[data-testid="stCheckbox"] label {
    color: #526b86 !important;
    font-size: 11px !important;
}

.st-key-reminder_form .stButton {
    display: flex !important;
    justify-content: flex-end !important;
}

.st-key-reminder_form .stButton > button {
    width: 168px !important;
    min-height: 36px !important;
    height: 36px !important;
    border-radius: 5px !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    margin-top: 0 !important;
}

/* ---------- INPUTS ---------- */
div[data-testid="stTextInput"] input,
div[data-testid="stDateInput"] input,
div[data-testid="stTimeInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    border: 1px solid #dbe3ec !important;
    border-radius: 5px !important;
    background: #ffffff !important;
    min-height: 35px !important;
    font-size: 12px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #a0aec0 !important;
}

/* ---------- BOTÕES ---------- */
.stButton > button {
    border-radius: 5px !important;

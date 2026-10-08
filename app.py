import streamlit as st
import pandas as pd
from datetime import datetime, date
from html import escape
import calendar
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
# CSS — VISUAL DA REFERÊNCIA (SEM RISCO DE SINTAXE)
# ============================================================
st.markdown("""
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

/* ===== MENU SUPERIOR — QUADRADINHOS / BOTÕES ===== */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 10px !important;
    align-items: center !important;
    margin: 8px 0 16px 0 !important;
    background: transparent !important;
}

div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 6px !important;
    height: 38px !important;
    padding: 0 16px !important;
    margin: 0 !important;
    color: #334155 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    cursor: pointer !important;
    box-shadow: 0 1px 3px rgba(15,23,42,.04) !important;
    transition: all .15s ease !important;
}

/* Oculta as bolinhas do Radio */
div[data-testid="stRadio"] > div[role="radiogroup"] label div[data-testid="stRadioButtonCustomIcon"],
div[data-testid="stRadio"] > div[role="radiogroup"] label input[type="radio"],
div[data-testid="stRadio"] > div[role="radiogroup"] label > div:first-child {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
    border-color: #cbd5e1 !important;
    color: #dc2638 !important;
}

/* Item Selecionado em Vermelho */
div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked),
div[data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"] {
    background-color: #dc2638 !important;
    border-color: #dc2638 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 6px rgba(220, 38, 56, 0.2) !important;
}

div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) p,
div[data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"] p,
div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) span,
div[data-testid="stRadio"] > div[role="radiogroup"] > label[aria-checked="true"] span {
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

/* ---------- FORMULÁRIO LEMBRETE ---------- */
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
    font-size: 11px !important;
    background: #ffffff !important;
}

.st-key-reminder_form div[data-testid="stCheckbox"] label {
    color: #526b86 !important;
    font-size: 11px !important;
}

/* ---------- INPUTS E BOTÕES ---------- */
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

.stButton > button {
    border-radius: 5px !important;
    border: 1px solid #dbe3ec !important;
    min-height: 35px !important;
    font-size: 12px !important;
    font-weight: 650 !important;
    background: #ffffff !important;
    color: #334155 !important;
}

.stButton > button[kind="primary"] {
    background: #dc2638 !important;
    border-color: #dc2638 !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    color: white !important;
    background: #c81f32 !important;
}

/* ---------- CALENDÁRIO CLICÁVEL ---------- */
.calendar-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 7px;
    padding: 15px 16px;
    box-shadow: 0 1px 4px rgba(15,23,42,.045);
}

.calendar-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #1e3a5f;
    font-size: 14px;
    font-weight: 750;
    margin-bottom: 13px;
}

.cal-grid-clickable {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 4px;
    text-align: center;
}

.cal-weekday-clickable {
    color: #94a3b8;
    font-size: 9px;
    font-weight: 700;
    padding-bottom: 5px;
}

.cal-empty {
    min-height: 31px;
}

.cal-link {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    min-height: 31px;
    color: #475569 !important;
    text-decoration: none !important;
    font-size: 10px;
    line-height: 21px;
}

.cal-number {
    width: 24px;
    height: 24px;
    line-height: 24px;
    border-radius: 50%;
}

.cal-number.today {
    background: #dc2638;
    color: #ffffff;
    font-weight: 800;
}

.cal-number.selected {
    outline: 2px solid #dc2638;
    outline-offset: 1px;
    font-weight: 800;
}

.cal-dot-red {
    width: 4px;
    height: 4px;
    background: #dc2638;
    border-radius: 50%;
    margin-top: 1px;
}

.calendar-selected {
    margin-top: 10px;
    background: #f8fafc;

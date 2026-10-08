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

/* ===== MENU SUPERIOR — BOTÕES EM CARD ARREDONDADO ===== */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 10px !important;
    align-items: center !important;
    margin: 8px 0 16px 0 !important;
    background: transparent !important;
}

/* Formatação base de cada item do menu */
div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    height: 42px !important;
    padding: 0 18px !important;
    margin: 0 !important;
    color: #1e293b !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    cursor: pointer !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
    transition: all 0.2s ease !important;
}

/* ESCONDE A BOLINHA DO RADIO COMPLETAMENTE */
div[data-testid="stRadio"] > div[role="radiogroup"] label div[data-testid="stRadioButtonCustomIcon"],
div[data-testid="stRadio"] > div[role="radiogroup"] label input[type="radio"],
div[data-testid="stRadio"] > div[role="radiogroup"] label > div:first-child {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Efeito ao passar o mouse */
div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
    border-color: #cbd5e1 !important;
    transform: translateY(-1px);
}

/* ABA SELECIONADA (Vermelho vibrante idêntico ao modelo da imagem) */
div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
    background-color: #dc2638 !important;
    border-color: #dc2638 !important;
    color: #ffffff !important;
    font-weight: 7

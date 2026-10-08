import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar
from dateutil.relativedelta import relativedelta
from supabase import create_client, Client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MSE | DP", page_icon="🔴", layout="wide")

# --- CSS CUSTOMIZADO PARA IDÊNTICO À FOTO DE REFERÊNCIA ---
st.markdown("""
    <style>
    /* Fundo geral do app em cinza suave */
    .stApp {
        background-color: #F3F4F6;
    }
    
    /* Cabeçalho Superior (Topbar) */
    .topbar-container {
        background-color: #1E293B;
        padding: 12px 24px;
        border-radius: 6px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    /* Cards/Blocos Brancos com Bordas e Sombras Leves */
    div[data-testid="stVerticalBlock"] > div.element-container:has(div.card-box) {
        width: 100%;
    }
    
    .card-box {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }

    /* Pílulas de Status OVALADAS */
    .badge-status-pendente {
        background-color: #FEF3C7;
        color: #D97706;
        padding: 4px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
        text-align: center;
    }

    .badge-status-concluido {
        background-color: #D1FAE5;
        color: #059669;
        padding: 4px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
        text-align: center;
    }

    /* Esconder marca de água e menus do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- CONEXÃO SUPABASE ---
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# --- CARREGAR COLABORADORES ---
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
    <div class="topbar-container">
        <div>
            <span style="font-size: 26px; font-weight: bold; color: #EF4444;">MSE</span>
            <span style="font-size: 22px; font-weight: bold; color: #FFFFFF; margin-left: 8px;">| DP</span>
        </div>
        <div>
            <span style="color: #4ADE80; font-weight: 600; font-size: 14px;">🟢 Nuvem Conectada</span>
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
aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "🔔 Meus Lembretes", 
    "📅 Calendário Coletivo", 
    "📋 Mural da Equipe", 
    "📊 Dashboard de Desempenho",
    "⚙️ Gerenciar Equipe"
])

# --- ABA 1: MEUS LEMBRETES ---
with aba1:
    col_principal, col_lateral = st.columns([2.3, 1])
    
    with col_principal:
        # Card 1: Form de Lembrete
        st.markdown("""
            <div class="card-box">
                <div style="font-size: 18px; font-weight: 700; color: #1E293B; margin-bottom: 12px;">
                    💬 O que você precisa lembrar?
                </div>
        """, unsafe_allow_html=True)
        
        c_input, c_data, c_hora = st.columns([2.5, 1.2, 1])
        with c_input:
            texto_lembrete = st.text_input("Lembrete", placeholder="Ex: Dia 08/02 às 09:00, subir e-mail", label_visibility="collapsed")
        with c_data:
            data_lembrete = st.date_input("Data", value=date.today(), label_visibility="collapsed")
        with c_hora:
            hora_lembrete = st.time_input("Horário", label_visibility="collapsed")
            
        col_check, col_btn = st.columns([2, 1.2])
        with col_check:
            recorrente = st.checkbox("Repetir este lembrete todo mês")
        with col_btn:
            btn_agendar = st.button("🗓️ Agendar Lembrete →", use_container_width=True, type="primary")
            
        if btn_agendar:
            if texto_lembrete:
                dt_completa = datetime.combine(data_lembrete, hora_lembrete).isoformat()
                dados_insert = {
                    "usuario": usuario_ativo,
                    "conteudo": texto_lembrete,
                    "data_hora": dt_completa,
                    "recorrente_mensal": recorrente,
                    "concluido": False
                }
                try:
                    supabase.table("lembretes").insert(dados_insert).execute()
                    st.success("Lembrete agendado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
            else:
                st.warning("Digite o texto do lembrete.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Card 2: Tabela de Lembretes Agendados
        st.markdown("""
            <div class="card-box">
                <div style="font-size: 18px; font-weight: 700; color: #1E293B; margin-bottom: 16px;">
                    📋 Seus Lembretes Agendados
                </div>
        """, unsafe_allow_html=True)
        
        res_lembretes = supabase.table("lembretes").select("*").eq("usuario", usuario_ativo).order("data_hora").execute()
        
        if res_lembretes.data:
            # Construção visual estilizada estilo tabela HTML idêntica à referência
            html_tabela = """
            <table style="width:100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px;">
                <thead>
                    <tr style="border-bottom: 2px solid #F1F5F9; text-align: left; color: #64748B; font-size: 13px;">
                        <th style="padding: 10px;">Data</th>
                        <th style="padding: 10px;">Horário</th>
                        <th style="padding: 10px;">Lembrete</th>
                        <th style="padding: 10px; text-align: center;">Status</th>
                    </tr>
                </thead>
                <tbody>
            """
            for item in res_lembretes.data:
                dt_obj = datetime.fromisoformat(item['data_hora'].replace('Z', ''))
                st_class = "badge-status-concluido" if item.get('concluido') else "badge-status-pendente"
                st_label = "Concluído" if item.get('concluido') else "Pendente"
                
                html_tabela += f"""
                    <tr style="border-bottom: 1px solid #F1F5F9;">
                        <td style="padding: 12px 10px; color: #334155;">{dt_obj.strftime('%d/%m/%Y')}</td>
                        <td style="padding: 12px 10px; color: #334155;">{dt_obj.strftime('%H:%M')}</td>
                        <td style="padding: 12px 10px; color: #334155; font-weight: 500;">{item['conteudo']}</td>
                        <td style="padding: 12px 10px; text-align: center;"><span class="{st_class}">{st_label}</span></td>
                    </tr>
                """
            html_tabela += "</tbody></table>"
            st.markdown(html_tabela, unsafe_allow_html=True)
        else:
            st.info(f"Nenhum lembrete agendado para {usuario_ativo}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_lateral:
        # Card Lateral 1: Próximo Lembrete
        res_prox = supabase.table("lembretes").select("*").eq("usuario", usuario_ativo).eq("concluido", False).order("data_hora").limit(1).execute()
        
        st.markdown("""
            <div style="background-color: #FEF2F2; border: 1px solid #FEE2E2; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                <div style="color: #DC2626; font-weight: 700; font-size: 15px; display: flex; align-items: center; justify-content: center; gap: 6px;">
                    <span>🔔</span> Próximo Lembrete
                </div>
        """, unsafe_allow_html=True)
        
        if res_prox.data:
            prox = res_prox.data[0]
            dt = datetime.fromisoformat(prox['data_hora'].replace('Z', ''))
            st.markdown(f"""
                <div style="font-size: 38px; font-weight: 800; color: #DC2626; margin: 8px 0;">{dt.strftime('%H:%M')}</div>
                <div style="color: #1F2937; font-weight: 600; font-size:

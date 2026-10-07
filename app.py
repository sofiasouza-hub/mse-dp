import streamlit as st
import pandas as pd
from datetime import datetime, date
from supabase import create_client, Client

# Configuração da Página
st.set_page_config(page_title="MSE | DP", page_icon="🔴", layout="wide")

# Estilização CSS Personalizada (Tema MSE DP)
st.markdown("""
    <style>
        .main { background-color: #F3F4F6; }
        .topbar {
            background-color: #1E293B;
            padding: 15px 25px;
            border-radius: 8px;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .logo-text { font-size: 26px; font-weight: bold; color: #DC2626; }
        .dept-text { font-size: 22px; font-weight: bold; color: #FFFFFF; margin-left: 10px; }
        .stButton>button {
            background-color: #DC2626;
            color: white;
            border-radius: 6px;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover { background-color: #B91C1C; color: white; }
    </style>
""", unsafe_allow_html=True)

# Conexão com Supabase
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# Buscar lista de colaboradores com salvaguarda
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
        <div>🟢 Nuvem Conectada</div>
    </div>
""", unsafe_allow_html=True)

col_top1, col_top2 = st.columns([3, 1])
with col_top2:
    idx_padrao = lista_equipe.index("SOFIA") if "SOFIA" in lista_equipe else 0
    usuario_ativo = st.selectbox("👤 Usuário Ativo", options=lista_equipe, index=idx_padrao)

# Garantir string válida
if not usuario_ativo:
    usuario_ativo = "SOFIA"

# --- NAVEGAÇÃO POR ABAS ---
aba1, aba2, aba3, aba4 = st.tabs(["🔴 Meus Lembretes", "📅 Calendário Coletivo", "📋 Mural da Equipe", "⚙️ Gerenciar Equipe"])

# --- ABA 1: MEUS LEMBRETES ---
with aba1:
    col_esq, col_dir = st.columns([2, 1])
    
    with col_esq:
        st.subheader("💬 O que você precisa lembrar?")
        
        c_texto, c_data, c_hora = st.columns([2, 1, 1])
        with c_texto:
            texto_lembrete = st.text_input("Lembrete", placeholder="Ex: Dia 08/02 às 09:00, subir e-mail")
        with c_data:
            data_lembrete = st.date_input("Data", value=date.today())
        with c_hora:
            hora_lembrete = st.time_input("Horário")
            
        recorrente = st.checkbox("Repetir este lembrete todo mês")
        
        if st.button("🗓️ Agendar Lembrete →"):
            if texto_lembrete:
                dt_completa = datetime.combine(data_lembrete, hora_lembrete).isoformat()
                supabase.table("lembretes").insert({
                    "usuario": usuario_ativo,
                    "conteudo": texto_lembrete,
                    "data_hora": dt_completa,
                    "recorrente_mensal": recorrente
                }).execute()
                st.success("Lembrete agendado com sucesso!")
                st.rerun()
            else:
                st.warning("Preencha o texto do lembrete.")

        st.markdown("---")
        st.subheader("📋 Seus Lembretes Agendados")
        
        res_lembretes = supabase.table("lembretes").select("*").eq("usuario", usuario_ativo).order("data_hora").execute()
        if res_lembretes.data:
            df = pd.DataFrame(res_lembretes.data)
            df['Data/Hora'] = pd.to_datetime(df['data_hora']).dt.strftime('%d/%m/%Y %H:%M')
            df['Status'] = df['concluido'].apply(lambda x: "🟢 Concluído" if x else "🟡 Pendente")
            st.dataframe(df[['Data/Hora', 'conteudo', 'Status']].rename(columns={'conteudo': 'Lembrete'}), use_container_width=True)
        else:
            st.info(f"Nenhum lembrete agendado para {usuario_ativo}")

    with col_dir:
        st.subheader("🔔 Próximo Lembrete")
        res_prox = supabase.table("lembretes").select("*").eq("usuario", usuario_ativo).eq("concluido", False).order("data_hora").limit(1).execute()
        if res_prox.data:
            prox = res_prox.data[0]
            dt = datetime.fromisoformat(prox['data_hora'].replace('Z', ''))
            st.error(f"⏰ **{dt.strftime('%H:%M')}** ({dt.strftime('%d/%m/%Y')})\n\n**{prox['conteudo']}**")
        else:
            st.success("Sem lembretes pendentes!")

# --- ABA 2: CALENDÁRIO COLETIVO ---
with aba2:
    st.subheader("📅 Calendário Coletivo do DP")
    dia_selecionado = st.date_input("Selecione um dia para adicionar recado da equipe", value=date.today())
    nota_texto = st.text_input("Nota ou recado para o dia selecionado")
    if st.button("Salvar no Calendário"):
        if nota_texto:
            supabase.table("notas_calendario").insert({
                "data": str(dia_selecionado),
                "autor": usuario_ativo,
                "nota": nota_texto
            }).execute()
            st.success("Nota adicionada ao calendário!")
            st.rerun()

    st.markdown("---")
    res_notas = supabase.table("notas_calendario").select("*").order("data", desc=True).execute()
    if res_notas.data:
        st.dataframe(pd.DataFrame(res_notas.data)[['data', 'autor', 'nota']].rename(columns={'data': 'Data', 'autor': 'Autor', 'nota': 'Recado'}), use_container_width=True)

# --- ABA 3: MURAL DA EQUIPE ---
with aba3:
    st.subheader("📋 Mural Transparente do DP")
    filtro_pessoa = st.selectbox("Filtrar visualização por colaborador:", ["Todos"] + lista_equipe)
    
    query = supabase.table("lembretes").select("*")
    if filtro_pessoa != "Todos":
        query = query.eq("usuario", filtro_pessoa)
    res_mural = query.order("data_hora", desc=True).execute()

    if res_mural.data:
        for item in res_mural.data:
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.write(f"👤 **{item['usuario']}**: {item['conteudo']} *(Agendado para: {datetime.fromisoformat(item['data_hora'].replace('Z', '')).strftime('%d/%m/%Y %H:%M')})*")
            with c2:
                st.write("🟢 Concluído" if item['concluido'] else "🟡 Pendente")
            with c3:
                if not item['concluido']:
                    if st.button("☑️ Marcar Feito", key=f"btn_{item['id']}"):
                        supabase.table("lembretes").update({"concluido": True}).eq("id", item['id']).execute()
                        st.rerun()

# --- ABA 4: GERENCIAR EQUIPE ---
with aba4:
    st.subheader("⚙️ Gerenciar Membros do DP")
    novo_nome = st.text_input("Nome do novo colaborador").upper()
    if st.button("➕ Adicionar à Equipe"):
        if novo_nome:
            try:
                supabase.table("colaboradores").insert({"nome": novo_nome}).execute()
                st.success(f"{novo_nome} adicionado com sucesso!")
                st.cache_data.clear()
                st.rerun()
            except Exception:
                st.error("Nome já cadastrado ou erro ao salvar.")

import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar
from supabase import create_client, Client

# Configuração da Página
st.set_page_config(page_title="MSE | DP", page_icon="🔴", layout="wide")

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
    <div style="background-color: #1E293B; padding: 14px 24px; border-radius: 8px; color: white; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div>
            <span style="font-size: 26px; font-weight: bold; color: #EF4444;">MSE</span>
            <span style="font-size: 22px; font-weight: bold; color: #FFFFFF; margin-left: 8px;">| DP</span>
        </div>
        <div>
            <span style="color: white; font-weight: bold;">🟢 Nuvem Conectada</span>
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
                }).execute()
                st.success("Lembrete agendado com sucesso!")
                st.rerun()
            else:
                st.warning("Digite o texto do lembrete.")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.subheader("📋 Seus Lembretes Agendados")
        res_lembretes = supabase.table("lembretes").select("*").eq("usuario", usuario_ativo).order("data_hora").execute()
        
        if res_lembretes.data:
            dados_tabela = []
            for item in res_lembretes.data:
                dt_obj = datetime.fromisoformat(item['data_hora'].replace('Z', ''))
                dados_tabela.append({
                    "Data": dt_obj.strftime('%d/%m/%Y'),
                    "Horário": dt_obj.strftime('%H:%M'),
                    "Lembrete": item['conteudo'],
                    "Status": "🟢 Concluído" if item['concluido'] else "🟡 Pendente"
                })
            df_exibir = pd.DataFrame(dados_tabela)
            st.dataframe(df_exibir, use_container_width=True, hide_index=True)
        else:
            st.info(f"Nenhum lembrete agendado para {usuario_ativo}")

    with col_lateral:
        # Card Lateral 1: Próximo Lembrete
        res_prox = supabase.table("lembretes").select("*").eq("usuario", usuario_ativo).eq("concluido", False).order("data_hora").limit(1).execute()
        
        st.markdown("""
            <div style="background-color: #FEF2F2; border: 1px solid #FECACA; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                <div style="color: #DC2626; font-weight: bold; font-size: 16px;">🔔 Próximo Lembrete</div>
        """, unsafe_allow_html=True)
        
        if res_prox.data:
            prox = res_prox.data[0]
            dt = datetime.fromisoformat(prox['data_hora'].replace('Z', ''))
            st.markdown(f"""
                <div style="font-size: 38px; font-weight: 800; color: #DC2626; margin: 8px 0;">{dt.strftime('%H:%M')}</div>
                <div style="color: #1F2937; font-weight: 600;">{prox['conteudo']}</div>
                <div style="color: #6B7280; font-size: 12px; margin-top: 5px;">Data: {dt.strftime('%d/%m/%Y')}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="font-size: 38px; font-weight: 800; color: #9CA3AF; margin: 8px 0;">--:--</div>
                <div style="color: #6B7280;">Sem lembretes pendentes</div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

        # Card Lateral 2: Calendário Visual
        st.markdown('<div style="background-color: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB;">', unsafe_allow_html=True)
        hoje = date.today()
        st.markdown(f'<div style="font-weight: bold; font-size: 16px; margin-bottom: 12px; color: #111827;">📅 {hoje.strftime("%B %Y").capitalize()}</div>', unsafe_allow_html=True)
        
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        grid_html = '<div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; text-align: center; font-size: 13px;">'
        for d in dias_semana:
            grid_html += f'<div style="font-weight: bold; color: #6B7280; padding-bottom: 4px;">{d}</div>'
            
        cal = calendar.monthcalendar(hoje.year, hoje.month)
        for semana in cal:
            for dia in semana:
                if dia == 0:
                    grid_html += '<div></div>'
                else:
                    is_today = (dia == hoje.day)
                    bg = "background-color: #DC2626; color: #FFFFFF; font-weight: bold;" if is_today else "color: #1F2937;"
                    grid_html += f'<div style="padding: 6px 0; border-radius: 50%; {bg}">{dia}</div>'
        grid_html += '</div>'
        
        st.markdown(grid_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

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
        st.dataframe(pd.DataFrame(res_notas.data)[['data', 'autor', 'nota']].rename(columns={'data': 'Data', 'autor': 'Autor', 'nota': 'Recado'}), use_container_width=True, hide_index=True)

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

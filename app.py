import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar
from dateutil.relativedelta import relativedelta
from supabase import create_client, Client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="MSE | DP", page_icon="🔴", layout="wide")

# --- CSS CUSTOMIZADO PARA FIDELIDADE VISUAL ---
st.markdown("""
    <style>
    /* Fundo da página e fontes */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Topbar estilizada */
    .topbar-container {
        background-color: #1E293B;
        padding: 12px 24px;
        border-radius: 8px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    /* Cards brancos customizados */
    .custom-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Badges de Status estilizados */
    .badge-pendente {
        background-color: #FEF3C7;
        color: #D97706;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
    }
    
    .badge-concluido {
        background-color: #D1FAE5;
        color: #059669;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
    }

    /* Esconder o cabeçalho padrão do Streamlit */
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
    col_principal, col_lateral = st.columns([2.2, 1])
    
    with col_principal:
        # Card 1: Criar Lembrete
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color: #1E293B; margin-top:0;'>💬 O que você precisa lembrar?</h4>", unsafe_allow_html=True)
        
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

        # Card 2: Lista de Lembretes Agendados
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color: #1E293B; margin-top:0;'>📋 Seus Lembretes Agendados</h4>", unsafe_allow_html=True)
        
        res_lembretes = supabase.table("lembretes").select("*").eq("usuario", usuario_ativo).order("data_hora").execute()
        
        if res_lembretes.data:
            dados_tabela = []
            for item in res_lembretes.data:
                dt_obj = datetime.fromisoformat(item['data_hora'].replace('Z', ''))
                dados_tabela.append({
                    "Data": dt_obj.strftime('%d/%m/%Y'),
                    "Horário": dt_obj.strftime('%H:%M'),
                    "Lembrete": item['conteudo'],
                    "Recorrência": "🔄 Mensal" if item.get('recorrente_mensal') else "📌 Único",
                    "Status": "Concluído" if item.get('concluido') else "Pendente"
                })
            df_exibir = pd.DataFrame(dados_tabela)
            
            # Formatação visual com badges
            def color_status(val):
                if val == 'Concluído':
                    return 'background-color: #D1FAE5; color: #059669; font-weight: bold;'
                return 'background-color: #FEF3C7; color: #D97706; font-weight: bold;'

            st.dataframe(
                df_exibir.style.map(color_status, subset=['Status']),
                use_container_width=True, 
                hide_index=True
            )
        else:
            st.info(f"Nenhum lembrete agendado para {usuario_ativo}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_lateral:
        # Card Lateral 1: Próximo Lembrete
        res_prox = supabase.table("lembretes").select("*").eq("usuario", usuario_ativo).eq("concluido", False).order("data_hora").limit(1).execute()
        
        st.markdown("""
            <div style="background-color: #FEF2F2; border: 1px solid #FECACA; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px;">
                <div style="color: #DC2626; font-weight: bold; font-size: 15px;">🔔 Próximo Lembrete</div>
        """, unsafe_allow_html=True)
        
        if res_prox.data:
            prox = res_prox.data[0]
            dt = datetime.fromisoformat(prox['data_hora'].replace('Z', ''))
            st.markdown(f"""
                <div style="font-size: 36px; font-weight: 800; color: #DC2626; margin: 6px 0;">{dt.strftime('%H:%M')}</div>
                <div style="color: #1F2937; font-weight: 600;">{prox['conteudo']}</div>
                <div style="color: #6B7280; font-size: 12px; margin-top: 4px;">Data: {dt.strftime('%d/%m/%Y')}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="font-size: 36px; font-weight: 800; color: #9CA3AF; margin: 6px 0;">--:--</div>
                <div style="color: #6B7280; font-size: 14px;">Sem lembretes pendentes</div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

        # Card Lateral 2: Calendário Interativo
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        hoje = date.today()
        st.markdown(f'<div style="font-weight: bold; font-size: 16px; margin-bottom: 12px; color: #111827;">📅 {hoje.strftime("%B %Y").capitalize()}</div>', unsafe_allow_html=True)
        
        # Mapeamento de lembretes e recados do mês para interatividade
        dict_eventos = {}
        
        # Busca Lembretes do Usuário
        res_lembr_mes = supabase.table("lembretes").select("*").eq("usuario", usuario_ativo).execute()
        if res_lembr_mes.data:
            for l in res_lembr_mes.data:
                try:
                    dt_l = datetime.fromisoformat(l['data_hora'].replace('Z', ''))
                    if dt_l.year == hoje.year and dt_l.month == hoje.month:
                        d = dt_l.day
                        dict_eventos.setdefault(d, []).append(f"📌 {dt_l.strftime('%H:%M')} - {l['conteudo']}")
                except Exception:
                    pass
                    
        # Busca Recados do Calendário Coletivo
        res_col_mes = supabase.table("notas_calendario").select("*").execute()
        if res_col_mes.data:
            for n in res_col_mes.data:
                try:
                    dt_n = datetime.strptime(n['data'], "%Y-%m-%d")
                    if dt_n.year == hoje.year and dt_n.month == hoje.month:
                        d = dt_n.day
                        dict_eventos.setdefault(d, []).append(f"📢 [{n.get('autor', 'Geral')}] {n['nota']}")
                except Exception:
                    pass

        # Exibição do Grid de Dias
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        grid_html = '<div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; text-align: center; font-size: 12px;">'
        for d in dias_semana:
            grid_html += f'<div style="font-weight: bold; color: #6B7280;">{d}</div>'
            
        cal = calendar.monthcalendar(hoje.year, hoje.month)
        for semana in cal:
            for dia in semana:
                if dia == 0:
                    grid_html += '<div></div>'
                else:
                    is_today = (dia == hoje.day)
                    has_event = dia in dict_eventos
                    
                    if is_today:
                        style = "background-color: #DC2626; color: white; border-radius: 50%; font-weight: bold;"
                    elif has_event:
                        style = "background-color: #3B82F6; color: white; border-radius: 50%; font-weight: bold;"
                    else:
                        style = "color: #374151;"
                        
                    grid_html += f'<div style="padding: 6px 0; {style}">{dia}</div>'
        grid_html += '</div>'
        
        st.markdown(grid_html, unsafe_allow_html=True)
        
        # Interatividade das Bolinhas do Calendário
        st.markdown("<hr style='margin: 15px 0 10px 0;'>", unsafe_allow_html=True)
        dias_com_evento = sorted(list(dict_eventos.keys()))
        if dias_com_evento:
            dia_clicado = st.selectbox("🔍 Clique/Selecione o dia marcado:", options=dias_com_evento, format_func=lambda d: f"Dia {d}")
            if dia_clicado:
                st.markdown(f"**Compromissos do Dia {dia_clicado}:**")
                for item_txt in dict_eventos[dia_clicado]:
                    st.write(f"- {item_txt}")
        else:
            st.caption("Nenhum evento agendado este mês.")
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- ABA 2: CALENDÁRIO COLETIVO ---
with aba2:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader("📅 Calendário Coletivo do DP")
    st.caption("Avisos, reuniões e eventos gerais visíveis para todo o setor.")
    
    dia_selecionado = st.date_input("Selecione a data:", value=date.today())
    nota_texto = st.text_input("Recado ou compromisso do setor:")
    if st.button("Salvar no Calendário", type="primary"):
        if nota_texto:
            supabase.table("notas_calendario").insert({
                "data": str(dia_selecionado),
                "autor": usuario_ativo,
                "nota": nota_texto
            }).execute()
            st.success("Nota gravada com sucesso!")
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    res_notas = supabase.table("notas_calendario").select("*").order("data", desc=True).execute()
    if res_notas.data:
        df_notas = pd.DataFrame(res_notas.data)[['data', 'autor', 'nota']]
        df_notas.columns = ['Data', 'Autor', 'Recado']
        st.dataframe(df_notas, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ABA 3: MURAL DA EQUIPE ---
with aba3:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
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
                dt_format = datetime.fromisoformat(item['data_hora'].replace('Z', '')).strftime('%d/%m/%Y %H:%M')
                rec_label = " (🔄 Repete todo mês)" if item.get('recorrente_mensal') else ""
                st.write(f"👤 **{item['usuario']}**: {item['conteudo']}{rec_label} *(Agendado: {dt_format})*")
            with c2:
                if item.get('concluido'):
                    st.markdown('<span class="badge-concluido">🟢 Concluído</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-pendente">🟡 Pendente</span>', unsafe_allow_html=True)
            with c3:
                if not item.get('concluido'):
                    if item['usuario'] == usuario_ativo:
                        if st.button("☑️ Concluir", key=f"btn_{item['id']}"):
                            # Reagendamento automático se for mensal
                            if item.get('recorrente_mensal'):
                                dt_atual = datetime.fromisoformat(item['data_hora'].replace('Z', ''))
                                dt_prox_mes = dt_atual + relativedelta(months=1)
                                supabase.table("lembretes").insert({
                                    "usuario": item['usuario'],
                                    "conteudo": item['conteudo'],
                                    "data_hora": dt_prox_mes.isoformat(),
                                    "recorrente_mensal": True,
                                    "concluido": False
                                }).execute()
                            
                            # Marca o atual como concluído
                            supabase.table("lembretes").update({"concluido": True}).eq("id", item['id']).execute()
                            st.success("Lembrete concluído!")
                            st.rerun()
                    else:
                        st.caption("🔒 Aprazável só pelo criador")
            st.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ABA 4: DASHBOARD DE DESEMPENHO ---
with aba4:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.subheader(f"📊 Dashboard de Desempenho - {usuario_ativo}")
    st.caption("Acompanhamento de metas e cumprimento de tarefas individuais.")
    
    res_dash = supabase.table("lembretes").select("*").eq("usuario", usuario_ativo).execute()
    
    if res_dash.data:
        df_dash = pd.DataFrame(res_dash.data)
        total_tarefas = len(df_dash)
        concluidas = len(df_dash[df_dash['concluido'] == True])
        pendentes = total_tarefas - concluidas
        taxa_sucesso = (concluidas / total_tarefas * 100) if total_tarefas > 0 else 0
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total de Lembretes", total_tarefas)
        m2.metric("Concluídos", concluidas)
        m3.metric("Pendentes", pendentes)
        m4.metric("Taxa de Cumprimento", f"{taxa_sucesso:.1f}%")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("##### Desempenho Visual")
        st.progress(taxa_sucesso / 100)
        
        if taxa_sucesso == 100:
            st.balloons()
            st.success("Parabéns! Todas as tarefas do mês foram concluídas!")
        elif taxa_sucesso >= 70:
            st.info("Excelente ritmo de entregas no setor!")
        else:
            st.warning("Atenção aos lembretes pendentes para o fechamento do mês.")
    else:
        st.info("Nenhum dado registrado para gerar métricas de desempenho ainda.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- ABA 5: GERENCIAR EQUIPE ---
with aba5:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

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

# Estilização CSS segura
css_lines = [
    "<style>",
    ".stApp { background: #f3f4f6; color: #1e293b; }",
    ".block-container { max-width: 1240px; padding: 16px 24px 28px 24px; }",
    "#MainMenu, footer, header { visibility: hidden; }",
    ".topbar { height: 58px; background: #1e293b; border-radius: 6px; padding: 0 18px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 6px rgba(15, 23, 42, .12); margin-bottom: 12px; }",
    ".brand { display: flex; align-items: center; gap: 10px; }",
    ".brand-mse { color: #ef233c; font-size: 27px; font-weight: 900; letter-spacing: -1.5px; }",
    ".brand-divider { color: #64748b; font-size: 21px; }",
    ".brand-dp { color: white; font-size: 16px; font-weight: 700; }",
    ".top-status { display: flex; align-items: center; gap: 20px; color: #e2e8f0; font-size: 12px; }",
    ".connected { color: #4ade80; font-weight: 600; }",
    "div[data-testid='stRadio'] > div[role='radiogroup'] { display: flex !important; flex-wrap: wrap !important; gap: 8px !important; margin: 8px 0 16px 0 !important; }",
    "div[data-testid='stRadio'] > div[role='radiogroup'] > label { display: inline-flex !important; align-items: center !important; justify-content: center !important; background: #ffffff !important; border: 1px solid #d9dee7 !important; border-radius: 6px !important; min-height: 36px !important; padding: 0 14px !important; margin: 0 !important; color: #334155 !important; cursor: pointer !important; font-size: 13px !important; font-weight: 600 !important; }",
    "div[data-testid='stRadio'] > div[role='radiogroup'] label input[type='radio'], div[data-testid='stRadio'] > div[role='radiogroup'] label div[data-testid='stRadioButtonCustomIcon'], div[data-testid='stRadio'] > div[role='radiogroup'] label > div:first-child { display: none !important; width: 0 !important; height: 0 !important; margin: 0 !important; }",
    "div[data-testid='stRadio'] > div[role='radiogroup'] > label:has(input:checked), div[data-testid='stRadio'] > div[role='radiogroup'] > label[aria-checked='true'] { background-color: #dc2638 !important; border-color: #dc2638 !important; color: #ffffff !important; font-weight: 700 !important; }",
    "div[data-testid='stRadio'] > div[role='radiogroup'] > label:has(input:checked) p, div[data-testid='stRadio'] > div[role='radiogroup'] > label[aria-checked='true'] p, div[data-testid='stRadio'] > div[role='radiogroup'] > label:has(input:checked) span, div[data-testid='stRadio'] > div[role='radiogroup'] > label[aria-checked='true'] span { color: #ffffff !important; }",
    ".card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 7px; padding: 15px 18px; margin-bottom: 12px; }",
    ".card-title { color: #1e3a5f; font-size: 15px; font-weight: 750; margin-bottom: 11px; }",
    ".reminder-table { width: 100%; border-collapse: collapse; font-size: 11px; }",
    ".reminder-table th { background: #f1f5f9; color: #64748b; text-align: left; padding: 8px 9px; font-size: 10px; }",
    ".reminder-table td { color: #334155; padding: 9px; border-bottom: 1px solid #edf2f7; }",
    ".badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 9px; font-weight: 750; }",
    ".badge-pendente { background: #fef3c7; color: #d97706; }",
    ".badge-concluido { background: #d1fae5; color: #059669; }",
    ".calendar-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 7px; padding: 15px 16px; }",
    ".calendar-head { display: flex; justify-content: space-between; align-items: center; color: #1e3a5f; font-size: 14px; font-weight: 750; margin-bottom: 13px; }",
    ".cal-grid-clickable { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; text-align: center; }",
    ".cal-weekday-clickable { color: #94a3b8; font-size: 9px; font-weight: 700; padding-bottom: 5px; }",
    ".cal-empty { min-height: 31px; }",
    ".cal-link { display: flex; flex-direction: column; align-items: center; justify-content: flex-start; min-height: 31px; color: #475569 !important; text-decoration: none !important; font-size: 10px; }",
    ".cal-number { width: 24px; height: 24px; line-height: 24px; border-radius: 50%; }",
    ".cal-number.today { background: #dc2638; color: #ffffff; font-weight: 800; }",
    ".cal-number.selected { outline: 2px solid #dc2638; outline-offset: 1px; font-weight: 800; }",
    ".cal-dot-red { width: 4px; height: 4px; background: #dc2638; border-radius: 50%; margin-top: 1px; }",
    ".calendar-selected { margin-top: 10px; background: #f8fafc; border: 1px solid #e5e7eb; border-left: 3px solid #dc2638; border-radius: 6px; padding: 10px 11px; }",
    ".soft-divider { height: 1px; background: #edf2f7; margin: 8px 0 12px; }",
    "</style>"
]
st.markdown("".join(css_lines), unsafe_allow_html=True)

# Supabase
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# Dados Colaboradores
@st.cache_data(ttl=5)
def get_colaboradores():
    try:
        res = supabase.table("colaboradores").select("nome").order("nome").execute()
        nomes = [item["nome"] for item in res.data] if res.data else []
        if not nomes:
            nomes = ["ANY", "BRUNA", "FERNANDA", "ISAAC", "MARIA", "NATALIA", "SOFIA"]
        return nomes
    except Exception:
        return ["ANY", "BRUNA", "FERNANDA", "ISAAC", "MARIA", "NATALIA", "SOFIA"]

lista_equipe = get_colaboradores()

# Topbar
st.html("<div class='topbar'><div class='brand'><span class='brand-mse'>MSE</span><span class='brand-divider'>|</span><span class='brand-dp'>DP</span></div><div class='top-status'><span class='connected'>● Nuvem Conectada</span><span>|</span><span>👤 Usuário: Sofia</span></div></div>")

# Usuário Ativo
idx_padrao = lista_equipe.index("SOFIA") if "SOFIA" in lista_equipe else 0
col_user, _ = st.columns([0.55, 4.45])
with col_user:
    usuario_ativo = st.selectbox("Usuário ativo", options=lista_equipe, index=idx_padrao, label_visibility="collapsed")

if not usuario_ativo:
    usuario_ativo = "SOFIA"

# Menu Principal
opcoes_menu = [
    "🔔  Meus Lembretes",
    "📅  Calendário Coletivo",
    "📋  Mural da Equipe",
    "📊  Dashboard",
    "⚙️  Gerenciar Equipe",
]

menu = st.radio("Navegação", opcoes_menu, horizontal=True, label_visibility="collapsed")

# Calendário Coletivo Helper
def montar_calendario_coletivo(hoje, eventos, dia_selecionado=None):
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    html = '<div class="cal-grid-clickable">'
    for nome_dia in dias_semana:
        html += f'<div class="cal-weekday-clickable">{nome_dia}</div>'

    cal = calendar.monthcalendar(hoje.year, hoje.month)
    for semana in cal:
        for dia in semana:
            if dia == 0:
                html += '<div class="cal-empty"></div>'
                continue
            tem_evento = dia in eventos
            eh_hoje = dia == hoje.day
            esta_selecionado = dia == dia_selecionado
            classes = ["cal-number"]
            if eh_hoje: classes.append("today")
            if esta_selecionado: classes.append("selected")
            numero = " ".join(classes)
            dot = '<div class="cal-dot-red"></div>' if tem_evento else ""
            href = f"?cal_day={dia}&cal_month={hoje.month}&cal_year={hoje.year}"
            html += f'<a class="cal-link" href="{href}"><div class="{numero}">{dia}</div>{dot}</a>'
    html += '</div>'
    return html

# ABA 1 — MEUS LEMBRETES
if menu == "🔔  Meus Lembretes":
    col_principal, col_lateral = st.columns([2.35, 1], gap="medium")
    
    with col_principal:
        with st.container(border=True):
            st.markdown("💬 **O que você precisa lembrar?**")
            texto_lembrete = st.text_input("Lembrete", placeholder="Ex: Dia 08/02 às 09:00, subir e-mail", label_visibility="collapsed")
            c_data, c_hora = st.columns(2)
            with c_data: data_lembrete = st.date_input("Data", value=date.today(), label_visibility="collapsed")
            with c_hora: hora_lembrete = st.time_input("Horário", value=datetime.now().time().replace(second=0, microsecond=0), label_visibility="collapsed")
            c_check, c_btn = st.columns([1.5, 1])
            with c_check: recorrente = st.checkbox("Repetir este lembrete todo mês")
            with c_btn: btn_agendar = st.button("🗓️ Agendar Lembrete →", use_container_width=True, type="primary")

            if btn_agendar:
                if texto_lembrete:
                    dt_completa = datetime.combine(data_lembrete, hora_lembrete).isoformat()
                    try:
                        supabase.table("lembretes").insert({
                            "usuario": usuario_ativo,
                            "conteudo": texto_lembrete,
                            "data_hora": dt_completa,
                            "recorrente_mensal": recorrente,
                            "concluido": False
                        }).execute()
                        st.success("Lembrete agendado!")
                        st.rerun()
                    except Exception as e: st.error(f"Erro: {e}")
                else: st.warning("Digite o texto.")

        try:
            res_lembretes = supabase.table("lembretes").select("*").eq("usuario", usuario_ativo).order("data_hora").execute()
        except Exception:
            res_lembretes = type("Obj", (), {"data": []})()

        linhas_tabela = ""
        for item in (res_lembretes.data or []):
            try:
                dt_obj = datetime.fromisoformat(item["data_hora"].replace("Z", ""))
                concluido = bool(item.get("concluido"))
                badge = '<span class="badge badge-concluido">Concluído</span>' if concluido else '<span class="badge badge-pendente">Pendente</span>'
                linhas_tabela += f'<tr><td>{escape(dt_obj.strftime("%d/%m/%Y"))}</td><td>{escape(dt_obj.strftime("%H:%M"))}</td><td>{escape(str(item.get("conteudo","")))}</td><td>{badge}</td></tr>'
            except Exception: continue

        if not linhas_tabela:
            linhas_tabela = '<tr><td colspan="4" style="text-align:center;color:#94a3b8;padding:18px;">Nenhum lembrete.</td></tr>'

        st.html(f'<div class="card"><div class="card-title">📋 &nbsp;Seus Lembretes Agendados</div><table class="reminder-table"><thead><tr><th>Data</th><th>Horário</th><th>Lembrete</th><th>Status</th></tr></thead><tbody>{linhas_tabela}</tbody></table></div>')

    with col_lateral:
        hoje = date.today()
        eventos_coletivos = {}
        try:
            res_col_mes = supabase.table("notas_calendario").select("*").execute()
            for nota in (res_col_mes.data or []):
                try:
                    dt_n = datetime.strptime(str(nota["data"]), "%Y-%m-%d")
                    if dt_n.year == hoje.year and dt_n.month == hoje.month:
                        eventos_coletivos.setdefault(dt_n.day, []).append({"nota": str(nota.get("nota", "")), "autor": str(nota.get("autor", "Geral"))})
                except Exception: continue
        except Exception: pass

        dia_param = st.query_params.get("cal_day")
        try: dia_selecionado = int(dia_param) if dia_param else None
        except Exception: dia_selecionado = None

        meses = ["", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        cal_html = montar_calendario_coletivo(hoje, eventos_coletivos, dia_selecionado)

        st.html(f'<div class="calendar-card"><div class="calendar-head"><span>📅 &nbsp;{meses[hoje.month]} {hoje.year}</span><span style="color:#64748b;">‹ &nbsp;&nbsp; ›</span></div>{cal_html}</div>')

        if dia_selecionado and dia_selecionado in eventos_coletivos:
            evs = "".join([f'<div style="font-size:11px;color:#475569;padding:4px 0;">📌 <b>{escape(e["nota"])}</b> <span style="color:#94a3b8;">({escape(e["autor"])})</span></div>' for e in eventos_coletivos[dia_selecionado]])
            st.html(f'<div class="calendar-selected"><div style="font-size:12px;font-weight:800;color:#1e3a5f;">📅 Dia {dia_selecionado}</div>{evs}</div>')

# ABA 2 — CALENDÁRIO COLETIVO
elif menu == "📅  Calendário Coletivo":
    st.markdown('<div class="card"><div class="card-title">📅 &nbsp;Calendário Coletivo do DP</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1: d_sel = st.date_input("Data", value=date.today())
    with c2: n_txt = st.text_input("Recado ou compromisso do setor", placeholder="Ex: Reunião do DP às 14:00")
    if st.button("💾  Salvar no Calendário", type="primary"):
        if n_txt:
            try:
                supabase.table("notas_calendario").insert({"data": str(d_sel), "autor": usuario_ativo, "nota": n_txt}).execute()
                st.success("Salvo com sucesso!")
                st.rerun()
            except Exception as e: st.error(f"Erro: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    try:
        res_n = supabase.table("notas_calendario").select("*").order("data", desc=True).execute()
        if res_n.data:
            df_n = pd.DataFrame(res_n.data)[["data", "autor", "nota"]]
            df_n.columns = ["Data", "Autor", "Recado"]
            st.dataframe(df_n, use_container_width=True, hide_index=True)
    except Exception: pass

# ABA 3 — MURAL DA EQUIPE
elif menu == "📋  Mural da Equipe":
    st.markdown('<div class="card"><div class="card-title">📋 &nbsp;Mural da Equipe</div>', unsafe_allow_html=True)
    f_p = st.selectbox("Filtrar por colaborador", ["Todos"] + lista_equipe)
    try:
        q = supabase.table("lembretes").select("*")
        if f_p != "Todos": q = q.eq("usuario", f_p)
        res_m = q.order("data_hora", desc=True).execute()
        if res_m.data:
            for item in res_m.data:
                c1, c2, c3 = st.columns([3.6, 1, 1])
                with c1: st.write(f"👤 **{item.get('usuario')}**: {item.get('conteudo')}")
                with c2: st.markdown('<span class="badge badge-concluido">Concluído</span>' if item.get("concluido") else '<span class="badge badge-pendente">Pendente</span>', unsafe_allow_html=True)
                with c3:
                    if not item.get("concluido"):
                        if item.get("usuario") == usuario_ativo:
                            if st.button("☑️ Concluir", key=f"b_{item['id']}"):
                                if item.get("recorrente_mensal"):
                                    dt_a = datetime.fromisoformat(item["data_hora"].replace("Z", ""))
                                    supabase.table("lembretes").insert({"usuario": item["usuario"], "conteudo": item["conteudo"], "data_hora": (dt_a + relativedelta(months=1)).isoformat(), "recorrente_mensal": True, "concluido": False}).execute()
                                supabase

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

/* ---------- INPUTS E BOTÕES ---------- */
div[data-testid="stTextInput"] input,
div[data-testid="stTimeInput"] input {
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

/* ---------- CALENDÁRIO INTERATIVO EMBUTIDO ---------- */
.form-cal-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 12px;
    margin-bottom: 10px;
}

.form-cal-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #1e3a5f;
    font-size: 13px;
    font-weight: 750;
    margin-bottom: 8px;
}

.form-cal-arrow {
    color: #64748b !important;
    font-size: 15px !important;
    text-decoration: none !important;
    font-weight: 700 !important;
    padding: 0 5px;
}

.form-cal-arrow:hover {
    color: #dc2638 !important;
}

.form-cal-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 3px;
    text-align: center;
}

.form-cal-weekday {
    color: #94a3b8;
    font-size: 9px;
    font-weight: 700;
    padding-bottom: 4px;
}

.form-cal-empty {
    min-height: 26px;
}

.form-cal-link {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 26px;
    color: #475569 !important;
    text-decoration: none !important;
    font-size: 10px;
}

.form-cal-num {
    width: 22px;
    height: 22px;
    line-height: 22px;
    border-radius: 50%;
}

.form-cal-num:hover {
    background: #fee2e2;
    color: #dc2638;
}

.form-cal-num.today {
    background: #f1f5f9;
    color: #dc2638;
    font-weight: 800;
}

.form-cal-num.selected {
    background: #dc2638;
    color: #ffffff;
    font-weight: 800;
}

/* ---------- TABELA ---------- */
.reminder-table {
    width: 100%;
    margin-top: 2px;
    border-collapse: collapse;
    font-family: Arial, sans-serif;
    font-size: 11px;
}

.reminder-table th {
    background: #f1f5f9;
    color: #64748b;
    text-align: left;
    font-size: 10px;
    font-weight: 750;
    padding: 8px 9px;
}

.reminder-table td {
    color: #334155;
    padding: 9px;
    border-bottom: 1px solid #edf2f7;
}

.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 9px;
    font-weight: 750;
}

.badge-pendente {
    background: #fef3c7;
    color: #d97706;
}

.badge-concluido {
    background: #d1fae5;
    color: #059669;
}

.soft-divider {
    height: 1px;
    background: #edf2f7;
    margin: 8px 0 12px;
}
</style>
"""), unsafe_allow_html=True)


# ============================================================
# SUPABASE
# ============================================================
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase = init_supabase()


# ============================================================
# DADOS
# ============================================================
@st.cache_data(ttl=5)
def get_colaboradores():
    try:
        res = (
            supabase
            .table("colaboradores")
            .select("nome")
            .order("nome")
            .execute()
        )
        nomes = [item["nome"] for item in res.data] if res.data else []

        if not nomes:
            nomes = ["ANY", "BRUNA", "FERNANDA", "ISAAC", "MARIA", "NATALIA", "SOFIA"]

        return nomes
    except Exception:
        return ["ANY", "BRUNA", "FERNANDA", "ISAAC", "MARIA", "NATALIA", "SOFIA"]


lista_equipe = get_colaboradores()


# ============================================================
# TOPBAR
# ============================================================
st.html("""
<div class="topbar">
    <div class="brand">
        <span class="brand-mse">MSE</span>
        <span class="brand-divider">|</span>
        <span class="brand-dp">DP</span>
    </div>
    <div class="top-status">
        <span class="connected">● Nuvem Conectada</span>
        <span>|</span>
        <span>👤 Usuário: Sofia</span>
    </div>
</div>
""")


# ============================================================
# USUÁRIO ATIVO
# ============================================================
idx_padrao = lista_equipe.index("SOFIA") if "SOFIA" in lista_equipe else 0

col_user, col_space = st.columns([0.55, 4.45])

with col_user:
    usuario_ativo = st.selectbox(
        "Usuário ativo",
        options=lista_equipe,
        index=idx_padrao,
        label_visibility="collapsed",
    )

if not usuario_ativo:
    usuario_ativo = "SOFIA"


# ============================================================
# MENU PRINCIPAL
# ============================================================
opcoes_menu = [
    "🔔  Meus Lembretes",
    "📅  Calendário Coletivo",
    "📋  Mural da Equipe",
    "📊  Dashboard",
    "⚙️  Gerenciar Equipe",
]

menu = st.radio(
    "Navegação",
    opcoes_menu,
    horizontal=True,
    label_visibility="collapsed",
)

st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)


# ============================================================
# FUNÇÕES — CALENDÁRIO
# ============================================================
def montar_calendario_coletivo(ano, mes, eventos, dia_selecionado=None):
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    hoje = date.today()

    html = '<div class="cal-grid-clickable">'

    for nome_dia in dias_semana:
        html += f'<div class="cal-weekday-clickable">{nome_dia}</div>'

    cal = calendar.monthcalendar(ano, mes)

    for semana in cal:
        for dia in semana:
            if dia == 0:
                html += '<div class="cal-empty"></div>'
                continue

            tem_evento = dia in eventos
            eh_hoje = (dia == hoje.day and mes == hoje.month and ano == hoje.year)
            esta_selecionado = dia == dia_selecionado

            classes = ["cal-number"]
            if eh_hoje:
                classes.append("today")
            if esta_selecionado:
                classes.append("selected")

            numero = " ".join(classes)

            dot = '<div class="cal-dot-red"></div>' if tem_evento else ""

            href = f"?cal_day={dia}&cal_month={mes}&cal_year={ano}"

            html += f"""
            <a class="cal-link" href="{href}" title="Ver compromissos do dia {dia}">
                <div class="{numero}">{dia}</div>
                {dot}
            </a>
            """

    html += "</div>"
    return html


def montar_mini_calendario_form(ano, mes, dia_sel):
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    hoje = date.today()

    html = '<div class="form-cal-grid">'

    for nome_dia in dias_semana:
        html += f'<div class="form-cal-weekday">{nome_dia}</div>'

    cal = calendar.monthcalendar(ano, mes)

    for semana in cal:
        for dia in semana:
            if dia == 0:
                html += '<div class="form-cal-empty"></div>'
                continue

            eh_hoje = (dia == hoje.day and mes == hoje.month and ano == hoje.year)
            esta_selecionado = (dia == dia_sel.day and mes == dia_sel.month and ano == dia_sel.year)

            classes = ["form-cal-num"]
            if esta_selecionado:
                classes.append("selected")
            elif eh_hoje:
                classes.append("today")

            numero = " ".join(classes)
            href = f"?f_day={dia}&f_month={mes}&f_year={ano}"

            html += f"""
            <a class="form-cal-link" href="{href}">
                <div class="{numero}">{dia}</div>
            </a>
            """

    html += "</div>"
    return html


# ============================================================
# ABA 1 — MEUS LEMBRETES
# ============================================================
if menu == "🔔  Meus Lembretes":

    col_principal, col_lateral = st.columns([2.35, 1], gap="medium")

    # --------------------------------------------------------
    # COLUNA PRINCIPAL
    # --------------------------------------------------------
    with col_principal:

        hoje = date.today()

        # Leitura dos parâmetros da URL para o mini-calendário do formulário
        f_m = int(st.query_params.get("f_month", hoje.month))
        f_y = int(st.query_params.get("f_year", hoje.year))

        if st.query_params.get("f_prev"):
            if f_m == 1:
                f_m = 12
                f_y -= 1
            else:
                f_m -= 1
            st.query_params["f_month"] = str(f_m)
            st.query_params["f_year"] = str(f_y)
            del st.query_params["f_prev"]
            st.rerun()

        if st.query_params.get("f_next"):
            if f_m == 12:
                f_m = 1
                f_y += 1
            else:
                f_m += 1
            st.query_params["f_month"] = str(f_m)
            st.query_params["f_year"] = str(f_y)
            del st.query_params["f_next"]
            st.rerun()

        f_day_param = st.query_params.get("f_day")
        try:
            dia_f_sel = int(f_day_param) if f_day_param else hoje.day
        except (TypeError, ValueError):
            dia_f_sel = hoje.day

        # Garante que o dia escolhido seja válido para o mês atual
        max_dias = calendar.monthrange(f_y, f_m)[1]
        if dia_f_sel > max_dias:
            dia_f_sel = max_dias

        data_lembrete_selecionada = date(f_y, f_m, dia_f_sel)

        meses = [
            "",
            "Janeiro", "Fevereiro", "Março", "Abril",
            "Maio", "Junho", "Julho", "Agosto",
            "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        # CARD — NOVO LEMBRETE
        with st.container(border=True, key="reminder_form"):

            st.markdown("""
            <div class="reminder-form-title">
                💬 &nbsp;O que você precisa lembrar?
            </div>
            """, unsafe_allow_html=True)

            texto_lembrete = st.text_input(
                "Lembrete",
                placeholder="Ex: Dia 08/02 às 09:00, subir e-mail",
                label_visibility="collapsed",
                key="lembrete_texto_v9",
            )

            col_cal_form, col_hora = st.columns([1.4, 1], gap="medium")

            with col_cal_form:
                mini_cal_html = montar_mini_calendario_form(f_y, f_m, data_lembrete_selecionada)
                st.html(f"""
                <div class="form-cal-card">
                    <div class="form-cal-head">
                        <span>📅 &nbsp;{meses[f_m]} {f_y} &nbsp;— <b style="color:#dc2638;">Dia {data_lembrete_selecionada.strftime('%d/%m/%Y')}</b></span>
                        <div>
                            <a href="?f_prev=1&f_month={f_m}&f_year={f_y}&f_day={dia_f_sel}" class="form-cal-arrow">‹</a>
                            <a href="?f_next=1&f_month={f_m}&f_year={f_y}&f_day={dia_f_sel}" class="form-cal-arrow">›</a>
                        </div>
                    </div>
                    {mini_cal_html}
                </div>
                """)

            with col_hora:
                hora_lembrete = st.time_input(
                    "Horário",
                    value=datetime.now().time().replace(
                        second=0,
                        microsecond=0,
                    ),
                    label_visibility="collapsed",
                    key="lembrete_hora_v9",
                )

                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

                recorrente = st.checkbox(
                    "Repetir este lembrete todo mês",
                    key="lembrete_recorrente_v9",
                )

                btn_agendar = st.button(
                    "🗓️  Agendar Lembrete →",
                    use_container_width=True,
                    type="primary",
                    key="lembrete_agendar_v9",
                )

            if btn_agendar:
                if texto_lembrete:
                    dt_completa = datetime.combine(
                        data_lembrete_selecionada,
                        hora_lembrete,
                    ).isoformat()

                    dados_insert = {
                        "usuario": usuario_ativo,
                        "conteudo": texto_lembrete,
                        "data_hora": dt_completa,
                        "recorrente_mensal": recorrente,
                        "concluido": False,
                    }

                    try:
                        supabase.table("lembretes").insert(dados_insert).execute()
                        st.success("Lembrete agendado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao salvar: {e}")
                else:
                    st.warning("Digite o texto do lembrete.")

        # ----------------------------------------------------
        # CARD — LEMBRETES AGENDADOS
        # ----------------------------------------------------
        try:
            res_lembretes = (
                supabase
                .table("lembretes")
                .select("*")
                .eq("usuario", usuario_ativo)
                .order("data_hora")
                .execute()
            )
        except Exception as e:
            res_lembretes = type("Obj", (), {"data": []})()
            st.error(f"Erro ao carregar lembretes: {e}")

        linhas_tabela = ""

        for item in (res_lembretes.data or []):
            try:
                dt_obj = datetime.fromisoformat(
                    item["data_hora"].replace("Z", "")
                )

                concluido = bool(item.get("concluido"))
                status = "Concluído" if concluido else "Pendente"
                badge_class = (
                    "badge badge-concluido"
                    if concluido
                    else "badge badge-pendente"
                )

                data_txt = escape(dt_obj.strftime("%d/%m/%Y"))
                hora_txt = escape(dt_obj.strftime("%H:%M"))
                lembrete_txt = escape(str(item.get("conteudo", "")))

                linhas_tabela += f"""
                <tr>
                    <td>{data_txt}</td>
                    <td>{hora_txt}</td>
                    <td>{lembrete_txt}</td>
                    <td><span class="{badge_class}">{status}</span></td>
                </tr>
                """
            except Exception:
                continue

        if not linhas_tabela:
            linhas_tabela = """
            <tr>
                <td colspan="4" style="text-align:center;color:#94a3b8;padding:18px;">
                    Nenhum lembrete agendado.
                </td>
            </tr>
            """

        st.html(f"""
        <div class="card">
            <div class="card-title">📋 &nbsp;Seus Lembretes Agendados</div>

            <table class="reminder-table">
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>Horário</th>
                        <th>Lembrete</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {linhas_tabela}
                </tbody>
            </table>
        </div>
        """)

    # --------------------------------------------------------
    # COLUNA LATERAL — CALENDÁRIO COLETIVO INTERATIVO
    # --------------------------------------------------------
    with col_lateral:
        cal_m = int(st.query_params.get("cal_month", hoje.month))
        cal_y = int(st.query_params.get("cal_year", hoje.year))

        if st.query_params.get("cal_prev"):
            if cal_m == 1:
                cal_m = 12
                cal_y -= 1
            else:
                cal_m -= 1
            st.query_params["cal_month"] = str(cal_m)
            st.query_params["cal_year"] = str(cal_y)
            del st.query_params["cal_prev"]
            st.rerun()

        if st.query_params.get("cal_next"):
            if cal_m == 12:
                cal_m = 1
                cal_y += 1
            else:
                cal_m += 1
            st.query_params["cal_month"] = str(cal_m)
            st.query_params["cal_year"] = str(cal_y)
            del st.query_params["cal_next"]
            st.rerun()

        eventos_coletivos = {}

        try:
            res_col_mes = (
                supabase
                .table("notas_calendario")
                .select("*")
                .execute()
            )

            for nota in (res_col_mes.data or []):
                try:
                    dt_nota = datetime.strptime(
                        str(nota["data"]),
                        "%Y-%m-%d",
                    )

                    if (
                        dt_nota.year == cal_y
                        and dt_nota.month == cal_m
                    ):
                        eventos_coletivos.setdefault(
                            dt_nota.day,
                            []
                        ).append({
                            "nota": str(nota.get("nota", "")),
                            "autor": str(nota.get("autor", "Geral")),
                        })
                except Exception:
                    continue

        except Exception:
            pass

        dia_param = st.query_params.get("cal_day")

        try:
            dia_selecionado = int(dia_param) if dia_param else None
        except (TypeError, ValueError):
            dia_selecionado = None

        if (
            dia_selecionado is not None
            and (
                dia_selecionado < 1
                or dia_selecionado > calendar.monthrange(
                    cal_y,
                    cal_m,
                )[1]
            )
        ):
            dia_selecionado = None

        nome_mes = meses[cal_m]

        calendario_html = montar_calendario_coletivo(
            cal_y,
            cal_m,
            eventos_coletivos,
            dia_selecionado,
        )

        st.html(f"""
        <div class="calendar-card">
            <div class="calendar-head">
                <span>📅 &nbsp;{nome_mes} {cal_y}</span>
                <div>
                    <a href="?cal_prev=1&cal_month={cal_m}&cal_year={cal_y}" class="calendar-arrow-btn">‹</a>
                    <a href="?cal_next=1&cal_month={cal_m}&cal_year={cal_y}" class="calendar-arrow-btn">›</a>
                </div>
            </div>
            {calendario_html}
        </div>
        """)

        if dia_selecionado is not None:
            compromissos = eventos_coletivos.get(
                dia_selecionado,
                []
            )

            if compromissos:
                eventos_html = ""

                for evento in compromissos:
                    nota = escape(evento["nota"])
                    autor = escape(evento["autor"])

                    eventos_html += f"""
                    <div class="calendar-event">
                        📌 <b>{nota}</b>
                        <span style="color:#94a3b8;">
                            — cadastrado por {autor}
                        </span>
                    </div>
                    """

                st.html(f"""
                <div class="calendar-selected">
                    <div class="calendar-selected-title">
                        📅 Compromissos do dia {dia_selecionado}
                    </div>
                    {eventos_html}
                </div>
                """)
            else:
                st.html(f"""
                <div class="calendar-selected">
                    <div class="calendar-selected-title">
                        📅 Dia {dia_selecionado}
                    </div>
                    <div class="calendar-event" style="color:#94a3b8;">
                        Nenhum compromisso coletivo marcado para este dia.
                    </div>
                </div>
                """)

# ============================================================
# ABA 2 — CALENDÁRIO COLETIVO
# ============================================================
elif menu == "📅  Calendário Coletivo":

    st.markdown(textwrap.dedent("""
    <div class="card">
        <div class="card-title">📅 &nbsp;Calendário Coletivo do DP</div>
        <div style="font-size:11px;color:#64748b;margin-bottom:12px;">
            Avisos, reuniões e eventos gerais visíveis para todo o setor.
        </div>
    </div>
    """), unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        dia_selecionado = st.date_input(
            "Data",
            value=date.today(),
            format="DD/MM/YYYY",
        )

    with col2:
        nota_texto = st.text_input(
            "Recado ou compromisso do setor",
            placeholder="Ex: Reunião do DP às 14:00",
        )

    if st.button(
        "💾  Salvar no Calendário",
        type="primary",
    ):
        if nota_texto:
            try:
                supabase.table("notas_calendario").insert({
                    "data": str(dia_selecionado),
                    "autor": usuario_ativo,
                    "nota": nota_texto,
                }).execute()

                st.success("Nota gravada com sucesso!")
                st.rerun()

            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.warning("Digite um recado ou compromisso.")

    st.markdown(textwrap.dedent("""
    <div class="card">
        <div class="card-title">📋 Recados cadastrados</div>
    </div>
    """), unsafe_allow_html=True)

    try:
        res_notas = (
            supabase
            .table("notas_calendario")
            .select("*")
            .order("data", desc=True)
            .execute()
        )

        if res_notas.data:
            for nota_item in res_notas.data:
                col_info, col_del = st.columns([4, 1])
                with col_info:
                    try:
                        data_br = datetime.strptime(str(nota_item.get("data")), "%Y-%m-%d").strftime("%d/%m/%Y")
                    except Exception:
                        data_br = str(nota_item.get("data"))

                    st.markdown(
                        f"🗓️ **{data_br}** — {nota_item.get('nota')} *(por {nota_item.get('autor')})*"
                    )
                with col_del:
                    if nota_item.get("autor") == usuario_ativo:
                        if st.button("🗑️ Apagar", key=f"del_nota_{nota_item['id']}"):
                            supabase.table("notas_calendario").delete().eq("id", nota_item["id"]).execute()
                            st.success("Recado apagado!")
                            st.rerun()
                    else:
                        st.caption("🔒 Somente o criador")
                st.markdown("<div class='soft-divider'></div>", unsafe_allow_html=True)
        else:
            st.info("Nenhum recado cadastrado.")

    except Exception as e:
        st.error(f"Erro ao carregar recados: {e}")


# ============================================================
# ABA 3 — MURAL DA EQUIPE
# ============================================================
elif menu == "📋  Mural da Equipe":

    with st.container(border=True, key="mural_card"):

        st.markdown("""
        <div class="card-title">📋 &nbsp;Mural da Equipe</div>
        """, unsafe_allow_html=True)

        filtro_pessoa = st.selectbox(
            "Filtrar por colaborador",
            ["Todos"] + lista_equipe,
            key="filtro_mural_sel"
        )

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        try:
            query = supabase.table("lembretes").select("*")

            if filtro_pessoa != "Todos":
                query = query.eq("usuario", filtro_pessoa)

            res_mural = query.order(
                "data_hora",
                desc=True,
            ).execute()

            if res_mural.data:

                for item in res_mural.data:

                    c1, c2, c3, c4 = st.columns([3.2, 0.9, 0.9, 0.9])

                    with c1:
                        try:
                            dt_format = datetime.fromisoformat(
                                item["data_hora"].replace("Z", "")
                            ).strftime("%d/%m/%Y %H:%M")
                        except Exception:
                            dt_format = ""

                        rec_label = (
                            " 🔄 Repete todo mês"
                            if item.get("recorrente_mensal")
                            else ""
                        )

                        st.markdown(
                            f"""
                            <div style="font-size:12px;color:#334155;padding-top:4px;">
                                👤 <b>{item.get("usuario","")}</b> —
                                {item.get("conteudo","")}
                                <span style="color:#94a3b8;">
                                    &nbsp;({dt_format}{rec_label})
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with c2:
                        if item.get("concluido"):
                            st.markdown(
                                '<span class="badge badge-concluido">Concluído</span>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                '<span class="badge badge-pendente">Pendente</span>',
                                unsafe_allow_html=True,
                            )

                    with c3:
                        if not item.get("concluido"):
                            if item.get("usuario") == usuario_ativo:
                                if st.button(
                                    "☑️ Concluir",
                                    key=f"btn_{item['id']}",
                                ):
                                    if item.get("recorrente_mensal"):
                                        dt_atual = datetime.fromisoformat(
                                            item["data_hora"].replace("Z", "")
                                        )
                                        dt_prox_mes = dt_atual + relativedelta(months=1)

                                        supabase.table("lembretes").insert({
                                            "usuario": item["usuario"],
                                            "conteudo": item["conteudo"],
                                            "data_hora": dt_prox_mes.isoformat(),
                                            "recorrente_mensal": True,
                                            "concluido": False,
                                        }).execute()

                                    supabase.table("lembretes").update(
                                        {"concluido": True}
                                    ).eq("id", item["id"]).execute()

                                    st.success("Lembrete concluído!")
                                    st.rerun()
                            else:
                                st.caption("🔒 Criador")

                    with c4:
                        if item.get("usuario") == usuario_ativo:
                            if st.button("🗑️ Apagar", key=f"del_mural_{item['id']}"):
                                supabase.table("lembretes").delete().eq("id", item["id"]).execute()
                                st.success("Lembrete removido!")
                                st.rerun()

                    st.markdown(
                        "<div class='soft-divider'></div>",
                        unsafe_allow_html=True,
                    )

            else:
                st.info("Nenhum lembrete encontrado.")

        except Exception as e:
            st.error(f"Erro ao carregar o mural: {e}")


# ============================================================
# ABA 4 — DASHBOARD
# ============================================================
elif menu == "📊  Dashboard":

    st.markdown(textwrap.dedent(f"""
    <div class="card">
        <div class="card-title">📊 &nbsp;Dashboard de Desempenho — {usuario_ativo}</div>
        <div style="font-size:11px;color:#64748b;margin-bottom:15px;">
            Acompanhamento das tarefas e lembretes individuais.
        </div>
    </div>
    """), unsafe_allow_html=True)

    try:
        res_dash = (
            supabase
            .table("lembretes")
            .select("*")
            .eq("usuario", usuario_ativo)
            .execute()
        )

        if res_dash.data:

            df_dash = pd.DataFrame(res_dash.data)

            total_tarefas = len(df_dash)
            concluidas = len(
                df_dash[df_dash["concluido"] == True]
            )
            pendentes = total_tarefas - concluidas

            taxa_sucesso = (
                concluidas / total_tarefas * 100
                if total_tarefas > 0
                else 0.0
            )

            m1, m2, m3, m4 = st.columns(4)

            m1.metric(
                "Total de Lembretes",
                total_tarefas,
            )

            m2.metric(
                "Concluídos",
                concluidas,
            )

            m3.metric(
                "Pendentes",
                pendentes,
            )

            m4.metric(
                "Taxa de Cumprimento",
                f"{taxa_sucesso:.1f}%",
            )

            st.markdown(
                "<div class='soft-divider'></div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                "**Desempenho Visual**",
            )

            st.progress(
                min(taxa_sucesso / 100, 1.0)
            )

            if taxa_sucesso == 100:
                st.success(
                    "Parabéns! Todas as tarefas foram concluídas!"
                )
            elif taxa_sucesso >= 70:
                st.info(
                    "Excelente ritmo de entregas no setor!"
                )
            else:
                st.warning(
                    "Atenção aos lembretes pendentes."
                )

        else:
            st.info(
                "Nenhum dado registrado para gerar métricas."
            )

    except Exception as e:
        st.error(f"Erro ao gerar dashboard: {e}")


# ============================================================
# ABA 5 — GERENCIAR EQUIPE
# ============================================================
elif menu == "⚙️  Gerenciar Equipe":

    st.markdown(textwrap.dedent("""
    <div class="card">
        <div class="card-title">⚙️ &nbsp;Gerenciar Membros do DP</div>
        <div style="font-size:11px;color:#64748b;margin-bottom:15px;">
            Cadastre novos membros que poderão utilizar o sistema.
        </div>
    </div>
    """), unsafe_allow_html=True)

    novo_nome = st.text_input(
        "Nome do novo colaborador",
        placeholder="Digite o nome",
    ).upper()

    if st.button(
        "➕  Adicionar à Equipe",
        type="primary",
    ):
        if novo_nome:

            try:
                supabase.table("colaboradores").insert({
                    "nome": novo_nome
                }).execute()

                st.success(
                    f"{novo_nome} adicionado com sucesso!"
                )

                st.cache_data.clear()
                st.rerun()

            except Exception:
                st.error(
                    "Nome já cadastrado ou erro ao salvar."
                )

        else:
            st.warning(
                "Digite o nome do colaborador."
            )

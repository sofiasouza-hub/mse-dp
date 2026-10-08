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
    min-height: 32px !important;
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

/* ---------- CALENDÁRIO LATERAL NATIVO ---------- */
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
    margin-bottom: 10px;
}

.cal-grid-header {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 2px;
    text-align: center;
    margin-bottom: 6px;
}

.cal-weekday {
    color: #94a3b8;
    font-size: 10px;
    font-weight: 700;
}

/* Botões do grid de dias do calendário */
div[data-testid="stColumn"] .cal-day-btn button {
    width: 100% !important;
    min-height: 28px !important;
    height: 28px !important;
    padding: 0 !important;
    font-size: 11px !important;
    border-radius: 50% !important;
    border: none !important;
    background: transparent !important;
    color: #475569 !important;
}

div[data-testid="stColumn"] .cal-day-btn-today button {
    width: 100% !important;
    min-height: 28px !important;
    height: 28px !important;
    padding: 0 !important;
    font-size: 11px !important;
    border-radius: 50% !important;
    background: #dc2638 !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    border: none !important;
}

div[data-testid="stColumn"] .cal-day-btn-event button {
    position: relative !important;
    color: #dc2638 !important;
    font-weight: 800 !important;
}

/* Botões de navegação < e > */
.cal-nav-btn button {
    min-height: 24px !important;
    height: 24px !important;
    padding: 0 8px !important;
    font-size: 12px !important;
    border-radius: 4px !important;
    border: 1px solid #e2e8f0 !important;
    color: #64748b !important;
    background: #ffffff !important;
}

.calendar-selected {
    margin-top: 10px;
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-left: 3px solid #dc2638;
    border-radius: 6px;
    padding: 10px 11px;
}

.calendar-selected-title {
    color: #1e3a5f;
    font-size: 12px;
    font-weight: 800;
    margin-bottom: 7px;
}

.calendar-event {
    color: #475569;
    font-size: 11px;
    padding: 4px 0;
    border-bottom: 1px solid #edf2f7;
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
# ABA 1 — MEUS LEMBRETES
# ============================================================
if menu == "🔔  Meus Lembretes":

    col_principal, col_lateral = st.columns([2.35, 1], gap="medium")

    # --------------------------------------------------------
    # COLUNA PRINCIPAL
    # --------------------------------------------------------
    with col_principal:

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

            col_data, col_hora = st.columns([1, 1], gap="small")

            with col_data:
                data_lembrete = st.date_input(
                    "Data",
                    value=date.today(),
                    label_visibility="collapsed",
                    key="lembrete_data_v9",
                )

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

            col_check, col_btn = st.columns([1.55, 1], gap="small")

            with col_check:
                recorrente = st.checkbox(
                    "Repetir este lembrete todo mês",
                    key="lembrete_recorrente_v9",
                )

            with col_btn:
                btn_agendar = st.button(
                    "🗓️  Agendar Lembrete →",
                    use_container_width=True,
                    type="primary",
                    key="lembrete_agendar_v9",
                )

            if btn_agendar:
                if texto_lembrete:
                    dt_completa = datetime.combine(
                        data_lembrete,
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
    # COLUNA LATERAL — CALENDÁRIO COLETIVO INTERATIVO NATIVO
    # --------------------------------------------------------
    with col_lateral:
        hoje = date.today()
        if "cal_month" not in st.session_state:
            st.session_state.cal_month = hoje.month
        if "cal_year" not in st.session_state:
            st.session_state.cal_year = hoje.year

        cal_m = st.session_state.cal_month
        cal_y = st.session_state.cal_year

        if "selected_day" not in st.session_state:
            st.session_state.selected_day = None

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

        meses = [
            "",
            "Janeiro", "Fevereiro", "Março", "Abril",
            "Maio", "Junho", "Julho", "Agosto",
            "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        nome_mes = meses[cal_m]

        # Card Branco unificado para o calendário
        with st.container():
            st.markdown('<div class="calendar-card">', unsafe_allow_html=True)
            col_tit, col_prev, col_next = st.columns([3.2, 0.4, 0.4])

            with col_tit:
                st.markdown(f'<div style="color:#1e3a5f;font-size:14px;font-weight:750;padding-top:2px;">📅 &nbsp;{nome_mes} {cal_y}</div>', unsafe_allow_html=True)

            with col_prev:
                st.markdown('<div class="cal-nav-btn">', unsafe_allow_html=True)
                if st.button("‹", key="btn_cal_prev"):
                    if st.session_state.cal_month == 1:
                        st.session_state.cal_month = 12
                        st.session_state.cal_year -= 1
                    else:
                        st.session_state.cal_month -= 1
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with col_next:
                st.markdown('<div class="cal-nav-btn">', unsafe_allow_html=True)
                if st.button("›", key="btn_cal_next"):
                    if st.session_state.cal_month == 12:
                        st.session_state.cal_month = 1
                        st.session_state.cal_year += 1
                    else:
                        st.session_state.cal_month += 1
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            # Cabeçalho dos dias da semana
            st.markdown("""
            <div class="cal-grid-header">
                <div class="cal-weekday">Seg</div>
                <div class="cal-weekday">Ter</div>
                <div class="cal-weekday">Qua</div>
                <div class="cal-weekday">Qui</div>
                <div class="cal-weekday">Sex</div>
                <div class="cal-weekday">Sáb</div>
                <div class="cal-weekday">Dom</div>
            </div>
            """, unsafe_allow_html=True)

            # Matriz de dias do mês
            cal = calendar.monthcalendar(cal_y, cal_m)

            for semana in cal:
                cols = st.columns(7)
                for idx, dia in enumerate(semana):
                    if dia != 0:
                        eh_hoje = (dia == hoje.day and cal_m == hoje.month and cal_y == hoje.year)
                        tem_evento = dia in eventos_coletivos

                        btn_class = "cal-day-btn-today" if eh_hoje else ("cal-day-btn-event" if tem_evento else "cal-day-btn")
                        
                        cols[idx].markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
                        if cols[idx].button(str(dia), key=f"cal_day_{cal_y}_{cal_m}_{dia}"):
                            st.session_state.selected_day = dia
                            st.rerun()
                        cols[idx].markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        dia_selecionado = st.session_state.selected_day

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
            df_notas = pd.DataFrame(res_notas.data)[
                ["data", "autor", "nota"]
            ]

            df_notas.columns = [
                "Data",
                "Autor",
                "Recado",
            ]

            st.dataframe(
                df_notas,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Nenhum recado cadastrado.")

    except Exception as e:
        st.error(f"Erro ao carregar recados: {e}")


# ============================================================
# ABA 3 — MURAL
# ============================================================
elif menu == "📋  Mural da Equipe":

    st.markdown(textwrap.dedent("""
    <div class="card">
        <div class="card-title">📋 &nbsp;Mural da Equipe</div>
    </div>
    """), unsafe_allow_html=True)

    filtro_pessoa = st.selectbox(
        "Filtrar por colaborador",
        ["Todos"] + lista_equipe,
    )

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

                c1, c2, c3 = st.columns([3.6, 1, 1])

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

                                    dt_prox_mes = (
                                        dt_atual +
                                        relativedelta(months=1)
                                    )

                                    supabase.table("lembretes").insert({
                                        "usuario": item["usuario"],
                                        "conteudo": item["conteudo"],
                                        "data_hora": dt_prox_mes.isoformat(),
                                        "recorrente_mensal": True,
                                        "concluido": False,
                                    }).execute()

                                supabase.table("lembretes").update(
                                    {"concluido": True}
                                ).eq(
                                    "id",
                                    item["id"],
                                ).execute()

                                st.success("Lembrete concluído!")
                                st.rerun()

                        else:
                            st.caption("🔒 Somente o criador")

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

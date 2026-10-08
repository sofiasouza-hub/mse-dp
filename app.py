import streamlit as st
import pandas as pd
from datetime import datetime, date
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
    max-width: 1380px;
    padding: 18px 28px 32px 28px;
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

/* ---------- MENU ---------- */
.nav-wrap {
    background: transparent;
    margin-bottom: 13px;
}

/* Radio horizontal usado como menu */
div[data-testid="stHorizontalBlock"] {
    gap: 10px;
}

div[role="radiogroup"] {
    gap: 8px !important;
    background: transparent !important;
}

div[role="radiogroup"] > label {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 5px !important;
    min-height: 38px !important;
    padding: 0 17px !important;
    box-shadow: 0 1px 2px rgba(15,23,42,.04);
    color: #475569 !important;
    font-weight: 600 !important;
    font-size: 12px !important;
}

div[role="radiogroup"] > label:hover {
    border-color: #cbd5e1 !important;
}

div[role="radiogroup"] > label:has(input:checked) {
    background: #dc2638 !important;
    border-color: #dc2638 !important;
    color: white !important;
    box-shadow: 0 2px 5px rgba(220,38,56,.18);
}

div[role="radiogroup"] > label input {
    display: none !important;
}

div[role="radiogroup"] > label > div:first-child {
    display: none !important;
}

/* ---------- CARDS ---------- */
.card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 7px;
    padding: 17px 18px;
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

.section-title {
    color: #1e3a5f;
    font-size: 15px;
    font-weight: 750;
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

.stButton > button:hover {
    border-color: #dc2638 !important;
    color: #dc2638 !important;
}

.stButton > button[kind="primary"]:hover {
    color: white !important;
    background: #c81f32 !important;
}

/* ---------- CHECKBOX ---------- */
div[data-testid="stCheckbox"] label {
    font-size: 11px !important;
    color: #64748b !important;
}

/* ---------- PRÓXIMO LEMBRETE ---------- */
.next-card {
    background: #fff7f7;
    border: 1px solid #f7d9dc;
    border-left: 3px solid #dc2638;
    border-radius: 7px;
    padding: 15px 17px;
    margin-bottom: 12px;
}

.next-label {
    color: #dc2638;
    font-size: 13px;
    font-weight: 750;
}

.next-time {
    color: #dc2638;
    font-size: 25px;
    font-weight: 800;
    line-height: 1.1;
    margin-top: 7px;
}

.next-text {
    color: #334155;
    font-size: 12px;
    font-weight: 650;
    margin-top: 4px;
}

/* ---------- CALENDÁRIO ---------- */
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

.calendar-arrow {
    color: #64748b;
    font-size: 16px;
}

.cal-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 4px;
    text-align: center;
}

.cal-weekday {
    color: #94a3b8;
    font-size: 9px;
    font-weight: 700;
    padding-bottom: 4px;
}

.cal-day {
    min-height: 25px;
    font-size: 10px;
    color: #475569;
    padding-top: 2px;
}

.cal-day-number {
    width: 22px;
    height: 22px;
    line-height: 22px;
    margin: auto;
    border-radius: 50%;
}

.cal-today {
    background: #dc2638;
    color: white;
    font-weight: 750;
}

.cal-dot {
    width: 4px;
    height: 4px;
    background: #dc2638;
    border-radius: 50%;
    margin: 1px auto 0;
}

/* ---------- TABELA ---------- */
.reminder-table {
    width: 100%;
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

.reminder-table td:nth-child(2),
.reminder-table th:nth-child(2) {
    width: 80px;
}

.reminder-table td:nth-child(4),
.reminder-table th:nth-child(4) {
    text-align: center;
    width: 90px;
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

/* ---------- MÉTRICAS ---------- */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 7px;
    padding: 12px;
}

div[data-testid="stMetricLabel"] {
    font-size: 11px !important;
}

/* ---------- TABELAS NATIVAS ---------- */
div[data-testid="stDataFrame"] {
    border-radius: 6px;
    overflow: hidden;
}

/* ---------- DIVISÓRIA ---------- */
.soft-divider {
    height: 1px;
    background: #edf2f7;
    margin: 8px 0 12px;
}

/* ---------- RESPONSIVO ---------- */
@media (max-width: 900px) {
    .block-container {
        padding: 12px;
    }

    .top-status {
        gap: 8px;
        font-size: 10px;
    }

    div[role="radiogroup"] {
        flex-wrap: wrap !important;
    }
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
st.markdown(textwrap.dedent("""
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
"""), unsafe_allow_html=True)


# ============================================================
# USUÁRIO ATIVO
# ============================================================
idx_padrao = lista_equipe.index("SOFIA") if "SOFIA" in lista_equipe else 0

# O seletor continua existindo para trocar de usuário,
# mas fica compacto logo abaixo da barra superior.
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
# FUNÇÃO — CALENDÁRIO
# ============================================================
def montar_calendario(hoje, dict_eventos):
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    html = '<div class="cal-grid">'

    for d in dias_semana:
        html += f'<div class="cal-weekday">{d}</div>'

    cal = calendar.monthcalendar(hoje.year, hoje.month)

    for semana in cal:
        for dia in semana:
            if dia == 0:
                html += '<div class="cal-day"></div>'
                continue

            is_today = dia == hoje.day
            has_event = dia in dict_eventos

            number_class = "cal-day-number cal-today" if is_today else "cal-day-number"

            html += f"""
                <div class="cal-day">
                    <div class="{number_class}">{dia}</div>
                    {"<div class='cal-dot'></div>" if has_event else ""}
                </div>
            """

    html += "</div>"
    return html


# ============================================================
# ABA 1 — MEUS LEMBRETES
# ============================================================
if menu == "🔔  Meus Lembretes":

    col_principal, col_lateral = st.columns([2.35, 1], gap="small")

    # --------------------------------------------------------
    # COLUNA PRINCIPAL
    # --------------------------------------------------------
    with col_principal:

        # CARD — NOVO LEMBRETE
        st.markdown(textwrap.dedent("""
        <div class="card">
            <div class="card-title">💬 &nbsp;O que você precisa lembrar?</div>
        """), unsafe_allow_html=True)

        texto_lembrete = st.text_input(
            "Lembrete",
            placeholder="Ex: Dia 08/02 às 09:00, subir e-mail",
            label_visibility="collapsed",
        )

        col_data, col_hora = st.columns([1, 1])

        with col_data:
            data_lembrete = st.date_input(
                "Data",
                value=date.today(),
                label_visibility="collapsed",
            )

        with col_hora:
            hora_lembrete = st.time_input(
                "Horário",
                value=datetime.now().time().replace(second=0, microsecond=0),
                label_visibility="collapsed",
            )

        col_check, col_btn = st.columns([1.55, 1])

        with col_check:
            recorrente = st.checkbox("Repetir este lembrete todo mês")

        with col_btn:
            btn_agendar = st.button(
                "🗓️  Agendar Lembrete →",
                use_container_width=True,
                type="primary",
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

        st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------------------------------
        # CARD — LEMBRETES AGENDADOS
        # ----------------------------------------------------
        st.markdown(textwrap.dedent("""
        <div class="card">
            <div class="card-title">📋 &nbsp;Seus Lembretes Agendados</div>
        """), unsafe_allow_html=True)

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

        if res_lembretes.data:

            html_tabela = """
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
            """

            for item in res_lembretes.data:
                try:
                    dt_obj = datetime.fromisoformat(
                        item["data_hora"].replace("Z", "")
                    )

                    concluido = bool(item.get("concluido"))
                    badge_class = (
                        "badge badge-concluido"
                        if concluido
                        else "badge badge-pendente"
                    )
                    status = "Concluído" if concluido else "Pendente"

                    html_tabela += f"""
                    <tr>
                        <td>{dt_obj.strftime("%d/%m/%Y")}</td>
                        <td>{dt_obj.strftime("%H:%M")}</td>
                        <td>{item.get("conteudo", "")}</td>
                        <td><span class="{badge_class}">{status}</span></td>
                    </tr>
                    """
                except Exception:
                    continue

            html_tabela += """
                </tbody>
            </table>
            """

            st.markdown(html_tabela, unsafe_allow_html=True)

        else:
            st.info(f"Nenhum lembrete agendado para {usuario_ativo}.")

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # COLUNA LATERAL
    # --------------------------------------------------------
    with col_lateral:

        # CARD — PRÓXIMO LEMBRETE
        try:
            res_prox = (
                supabase
                .table("lembretes")
                .select("*")
                .eq("usuario", usuario_ativo)
                .eq("concluido", False)
                .order("data_hora")
                .limit(1)
                .execute()
            )
        except Exception:
            res_prox = type("Obj", (), {"data": []})()

        if res_prox.data:
            prox = res_prox.data[0]
            dt = datetime.fromisoformat(
                prox["data_hora"].replace("Z", "")
            )

            st.markdown(textwrap.dedent(f"""
            <div class="next-card">
                <div class="next-label">🔔 &nbsp;Próximo Lembrete</div>
                <div class="next-time">{dt.strftime("%H:%M")}</div>
                <div class="next-text">{prox.get("conteudo", "")}</div>
            </div>
            """), unsafe_allow_html=True)

        else:
            st.markdown(textwrap.dedent("""
            <div class="next-card">
                <div class="next-label">🔔 &nbsp;Próximo Lembrete</div>
                <div class="next-time" style="color:#94a3b8;">--:--</div>
                <div class="next-text" style="color:#64748b;">
                    Sem lembretes pendentes
                </div>
            </div>
            """), unsafe_allow_html=True)

        # ----------------------------------------------------
        # CALENDÁRIO
        # ----------------------------------------------------
        hoje = date.today()
        dict_eventos = {}

        try:
            res_lembr_mes = (
                supabase
                .table("lembretes")
                .select("*")
                .eq("usuario", usuario_ativo)
                .execute()
            )

            for l in res_lembr_mes.data or []:
                try:
                    dt_l = datetime.fromisoformat(
                        l["data_hora"].replace("Z", "")
                    )

                    if dt_l.year == hoje.year and dt_l.month == hoje.month:
                        dict_eventos.setdefault(dt_l.day, []).append(
                            f"📌 {dt_l.strftime('%H:%M')} - {l.get('conteudo', '')}"
                        )
                except Exception:
                    pass

        except Exception:
            pass

        try:
            res_col_mes = (
                supabase
                .table("notas_calendario")
                .select("*")
                .execute()
            )

            for n in res_col_mes.data or []:
                try:
                    dt_n = datetime.strptime(
                        n["data"],
                        "%Y-%m-%d",
                    )

                    if dt_n.year == hoje.year and dt_n.month == hoje.month:
                        dict_eventos.setdefault(dt_n.day, []).append(
                            f"📢 [{n.get('autor', 'Geral')}] {n.get('nota', '')}"
                        )
                except Exception:
                    pass

        except Exception:
            pass

        # Nome do mês em português
        meses = [
            "",
            "Janeiro", "Fevereiro", "Março", "Abril",
            "Maio", "Junho", "Julho", "Agosto",
            "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        nome_mes = meses[hoje.month]

        st.markdown(textwrap.dedent(f"""
        <div class="calendar-card">
            <div class="calendar-head">
                <span>📅 &nbsp;{nome_mes} {hoje.year}</span>
                <span class="calendar-arrow">‹ &nbsp;&nbsp; ›</span>
            </div>
            {montar_calendario(hoje, dict_eventos)}
        </div>
        """), unsafe_allow_html=True)

        # Seleção para visualizar os compromissos
        dias_com_evento = sorted(dict_eventos.keys())

        if dias_com_evento:
            dia_clicado = st.selectbox(
                "Ver compromissos",
                options=dias_com_evento,
                format_func=lambda d: f"Dia {d}",
                label_visibility="collapsed",
            )

            if dia_clicado:
                st.markdown(
                    f"<div class='soft-divider'></div><b>Compromissos do dia {dia_clicado}</b>",
                    unsafe_allow_html=True,
                )

                for item_txt in dict_eventos[dia_clicado]:
                    st.caption(item_txt)


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

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(textwrap.dedent("""
    <div class="card">
        <div class="section-title">📋 Recados cadastrados</div>
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

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ABA 3 — MURAL
# ============================================================
elif menu == "📋  Mural da Equipe":

    st.markdown(textwrap.dedent("""
    <div class="card">
        <div class="card-title">📋 &nbsp;Mural da Equipe</div>
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

    st.markdown("</div>", unsafe_allow_html=True)


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

    st.markdown("</div>", unsafe_allow_html=True)


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

    st.markdown("</div>", unsafe_allow_html=True)

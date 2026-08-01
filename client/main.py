import os
import re
from io import BytesIO

import requests
import streamlit as st
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "").rstrip("/")
BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

st.set_page_config(
    page_title="TutorRAG",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLING
# ============================================================

st.markdown(
    """
    <style>
    /* ---------- Global ---------- */
    :root {
        --primary: #4f46e5;
        --primary-dark: #4338ca;
        --primary-soft: #eef2ff;
        --text: #0f172a;
        --muted: #64748b;
        --border: #e2e8f0;
        --surface: #ffffff;
        --surface-soft: #f8fafc;
        --success: #059669;
        --danger: #dc2626;
    }

    .stApp {
        background: #f8fafc;
        color: var(--text);
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Hide Streamlit chrome where it adds visual noise */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* ---------- Typography ---------- */
    h1, h2, h3, h4 {
        color: var(--text) !important;
        letter-spacing: -0.03em;
    }

    p, label, .stMarkdown {
        color: var(--text);
    }

    .muted-text {
        color: var(--muted);
        font-size: 0.97rem;
        line-height: 1.65;
    }

    /* ---------- Navbar ---------- */
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.85rem 1.15rem;
        margin-bottom: 2rem;
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid var(--border);
        border-radius: 18px;
        box-shadow: 0 8px 30px rgba(15, 23, 42, 0.05);
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--text);
    }

    .brand-mark {
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: var(--primary-soft);
        font-size: 1.15rem;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.35rem 0.65rem;
        border-radius: 999px;
        background: var(--primary-soft);
        color: var(--primary-dark);
        font-size: 0.78rem;
        font-weight: 700;
    }

    /* ---------- Hero ---------- */
    .hero-wrap {
        padding: 2rem 0 1rem;
    }

    .eyebrow {
        display: inline-block;
        margin-bottom: 0.8rem;
        padding: 0.45rem 0.8rem;
        border-radius: 999px;
        background: var(--primary-soft);
        color: var(--primary-dark);
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .hero-title {
        font-size: clamp(2.8rem, 6vw, 5rem);
        line-height: 0.98;
        font-weight: 850;
        margin: 0;
        max-width: 700px;
    }

    .hero-title span {
        color: var(--primary);
    }

    .hero-copy {
        margin-top: 1.25rem;
        max-width: 630px;
        color: var(--muted);
        font-size: 1.12rem;
        line-height: 1.75;
    }

    .hero-card {
        min-height: 390px;
        padding: 1.15rem;
        border-radius: 24px;
        background: linear-gradient(145deg, #ffffff, #f1f5f9);
        border: 1px solid var(--border);
        box-shadow: 0 24px 60px rgba(15, 23, 42, 0.09);
    }

    .window-bar {
        display: flex;
        align-items: center;
        gap: 0.35rem;
        padding-bottom: 0.9rem;
        border-bottom: 1px solid var(--border);
    }

    .window-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #cbd5e1;
    }

    .preview-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 1rem;
    }

    .preview-title {
        font-weight: 800;
        font-size: 1rem;
    }

    .preview-badge {
        padding: 0.3rem 0.55rem;
        border-radius: 8px;
        background: #dcfce7;
        color: #166534;
        font-size: 0.72rem;
        font-weight: 800;
    }

    .document-card {
        margin-top: 1rem;
        padding: 1rem;
        border-radius: 16px;
        background: #ffffff;
        border: 1px solid var(--border);
    }

    .document-row {
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }

    .document-icon {
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: #fee2e2;
        font-size: 1rem;
    }

    .document-name {
        font-weight: 750;
        font-size: 0.92rem;
    }

    .document-meta {
        color: var(--muted);
        font-size: 0.76rem;
        margin-top: 0.15rem;
    }

    .chat-bubble {
        margin-top: 0.9rem;
        padding: 0.9rem 1rem;
        border-radius: 16px;
        font-size: 0.86rem;
        line-height: 1.55;
    }

    .chat-user {
        background: var(--primary-soft);
        margin-left: 2rem;
    }

    .chat-ai {
        background: #ffffff;
        border: 1px solid var(--border);
        margin-right: 2rem;
    }

    /* ---------- Feature cards ---------- */
    .section-heading {
        margin-top: 4rem;
        margin-bottom: 1.4rem;
    }

    .section-title {
        font-size: 2rem;
        font-weight: 850;
        margin-bottom: 0.35rem;
    }

    .section-copy {
        color: var(--muted);
        max-width: 650px;
    }

    .feature-card {
        min-height: 190px;
        padding: 1.3rem;
        border-radius: 18px;
        background: var(--surface);
        border: 1px solid var(--border);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .feature-icon {
        width: 42px;
        height: 42px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--primary-soft);
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .feature-copy {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.55;
    }

    /* ---------- App surfaces ---------- */
    .page-header {
        padding: 0.3rem 0 1.4rem;
    }

    .page-title {
        font-size: 2.25rem;
        font-weight: 850;
        margin: 0;
    }

    .page-subtitle {
        color: var(--muted);
        margin-top: 0.35rem;
    }

    .stat-card {
        padding: 1rem 1.1rem;
        border-radius: 16px;
        background: var(--surface);
        border: 1px solid var(--border);
    }

    .stat-label {
        font-size: 0.78rem;
        color: var(--muted);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .stat-value {
        margin-top: 0.2rem;
        font-size: 1.7rem;
        font-weight: 850;
    }

    .panel {
        padding: 1.25rem;
        border-radius: 18px;
        background: var(--surface);
        border: 1px solid var(--border);
        box-shadow: 0 8px 30px rgba(15, 23, 42, 0.04);
    }

    .soft-panel {
        padding: 1.25rem;
        border-radius: 18px;
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        border: 1px solid var(--border);
    }

    .empty-state {
        text-align: center;
        padding: 3rem 1.5rem;
        border: 1px dashed #cbd5e1;
        border-radius: 18px;
        background: #ffffff;
    }

    .empty-icon {
        font-size: 2rem;
        margin-bottom: 0.7rem;
    }

    .empty-title {
        font-size: 1.05rem;
        font-weight: 800;
    }

    .empty-copy {
        color: var(--muted);
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }

    /* ---------- Streamlit buttons ---------- */
    .stButton > button,
    .stFormSubmitButton > button {
        border-radius: 12px !important;
        font-weight: 750 !important;
        min-height: 44px;
        border: 1px solid var(--border) !important;
        transition: all 0.18s ease !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
    }

    /* Primary buttons */
    .stButton > button[kind="primary"],
    .stFormSubmitButton > button[kind="primary"] {
        background: var(--primary) !important;
        color: white !important;
        border-color: var(--primary) !important;
    }

    /* ---------- Inputs ---------- */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border-color: var(--border) !important;
        background: white !important;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #a5b4fc !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12) !important;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
    }

    .sidebar-brand {
        padding: 0.4rem 0 1.1rem;
        font-size: 1.15rem;
        font-weight: 850;
    }

    .profile-card {
        padding: 1rem;
        border-radius: 16px;
        background: var(--surface-soft);
        border: 1px solid var(--border);
        margin-bottom: 1rem;
    }

    .profile-name {
        font-weight: 800;
        font-size: 0.95rem;
    }

    .profile-role {
        margin-top: 0.2rem;
        color: var(--muted);
        font-size: 0.8rem;
    }

    /* ---------- Chat ---------- */
    [data-testid="stChatMessage"] {
        border-radius: 16px;
        border: 1px solid var(--border);
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
        background: #ffffff;
    }

    /* ---------- Tabs ---------- */
    button[data-baseweb="tab"] {
        font-weight: 750;
    }

    /* ---------- Footer ---------- */
    .footer {
        text-align: center;
        color: var(--muted);
        font-size: 0.82rem;
        margin-top: 4rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================


def init_state():
    defaults = {
        "page": "landing",
        "authenticated": False,
        "username": "",
        "password": "",
        "role": "",
        "grade": 0,
        "chat_messages": [],
        "generated_quiz": None,
        "quiz_result": None,
        "quiz_history": None,
    }

    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


init_state()


# ============================================================
# HELPERS
# ============================================================


def auth():
    return HTTPBasicAuth(
        st.session_state.username,
        st.session_state.password,
    )


def api(method, path, **kwargs):
    if not BACKEND_URL:
        raise RuntimeError("BACKEND_URL is not configured.")

    return requests.request(
        method,
        f"{BACKEND_URL}{path}",
        auth=auth(),
        timeout=60,
        **kwargs,
    )


def logout():
    st.session_state.clear()
    st.session_state.page = "landing"
    st.rerun()


def asset_path(filename):
    return os.path.join(ASSETS_DIR, filename)


def image_exists(filename):
    return os.path.exists(asset_path(filename))


def render_brand():
    st.markdown(
        """
        <div class="topbar">
            <div class="brand">
                <div class="brand-mark">🎓</div>
                <div>TutorRAG</div>
            </div>
            <div class="pill">RAG-powered learning</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="footer">
            TutorRAG · Learn from your own documents with AI
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat(label, value):
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_parsed_quiz(raw):
    blocks = re.split(r"(Question \d+:)", raw)[1:]
    questions = []

    for i in range(0, len(blocks), 2):
        lines = blocks[i + 1].strip().split("\n")
        if not lines:
            continue

        q_text = lines[0]
        options = [line for line in lines if re.match(r"[A-Z]\)", line)]
        questions.append({"q": q_text, "opts": options})

    return questions


# ============================================================
# LANDING PAGE
# ============================================================


def landing_page():
    render_brand()

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
        st.markdown('<div class="eyebrow">Your documents. Your tutor.</div>', unsafe_allow_html=True)
        st.markdown(
            '<h1 class="hero-title">Turn your notes into a <span>personal AI tutor.</span></h1>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="hero-copy">Upload textbooks and notes, ask questions grounded in your material, generate quizzes, and keep track of your learning progress.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        cta1, cta2 = st.columns([1, 1], gap="small")
        with cta1:
            if st.button("🚀 Get Started", type="primary", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()
        with cta2:
            if st.button("Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

        st.markdown(
            '<div class="muted-text" style="margin-top:1rem">Built with FastAPI · LangChain · RAG · LLMs</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown(
            """
            <div class="hero-card">
                <div class="window-bar">
                    <div class="window-dot"></div>
                    <div class="window-dot"></div>
                    <div class="window-dot"></div>
                </div>
                <div class="preview-header">
                    <div class="preview-title">AI Tutor Workspace</div>
                    <div class="preview-badge">Ready</div>
                </div>
                <div class="document-card">
                    <div class="document-row">
                        <div class="document-icon">📄</div>
                        <div>
                            <div class="document-name">Physics — Chapter 3.pdf</div>
                            <div class="document-meta">Indexed and ready for questions</div>
                        </div>
                    </div>
                </div>
                <div class="chat-bubble chat-user">
                    What is Newton's second law according to my notes?
                </div>
                <div class="chat-bubble chat-ai">
                    <strong>AI Tutor</strong><br>
                    Newton's second law states that the net force acting on an object is equal to its mass multiplied by its acceleration: <strong>F = ma</strong>.
                </div>
                <div class="chat-bubble" style="background:#f8fafc;border:1px dashed #cbd5e1;color:#64748b;">
                    ✨ Ask another question...
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-heading">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Everything you need to learn from your material</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">A focused learning workspace built around the documents you already study from.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    features = [
        ("📚", "Document Q&A", "Upload notes or textbooks and ask questions using answers grounded in your material."),
        ("💬", "AI Tutor Chat", "Have a conversational study session instead of searching through long documents manually."),
        ("📝", "Quiz Generator", "Generate quizzes from your selected topic and test yourself immediately."),
        ("📈", "Quiz History", "Review past attempts, compare your answers, and identify topics that need more practice."),
    ]

    cols = st.columns(4, gap="medium")
    for col, (icon, title, copy) in zip(cols, features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-copy">{copy}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-heading">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">How it works</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Go from raw study material to active learning in three simple steps.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    steps = [
        ("01", "Upload", "Teachers upload PDF study material and organize it by grade."),
        ("02", "Ask & practice", "Students ask questions and generate quizzes from the available material."),
        ("03", "Review", "Use quiz history to see results and revisit areas that need more work."),
    ]

    cols = st.columns(3, gap="medium")
    for col, (number, title, copy) in zip(cols, steps):
        with col:
            st.markdown(
                f"""
                <div class="soft-panel">
                    <div class="pill">Step {number}</div>
                    <h3 style="margin-top:0.9rem">{title}</h3>
                    <div class="feature-copy">{copy}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    render_footer()


# ============================================================
# LOGIN
# ============================================================


def login_page():
    render_brand()

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown(
            """
            <div style="padding:3rem 1rem 0 0;">
                <div class="eyebrow">Welcome back</div>
                <h1 class="page-title" style="font-size:3rem;">Continue your learning journey.</h1>
                <div class="hero-copy">Sign in to access your AI tutor, quizzes, and learning history.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if image_exists("login.jpg"):
            st.image(asset_path("login.jpg"), use_container_width=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### 🔐 Sign in")
        st.markdown('<div class="muted-text">Use your TutorRAG account to continue.</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("Login", type="primary", use_container_width=True)

            if submitted:
                try:
                    r = requests.get(
                        f"{BACKEND_URL}/login",
                        auth=HTTPBasicAuth(username, password),
                        timeout=30,
                    )

                    if r.status_code == 200:
                        data = r.json()
                        st.session_state.update(
                            {
                                "authenticated": True,
                                "username": username,
                                "password": password,
                                "role": data["role"],
                                "grade": data.get("grade", 0),
                                "page": "app",
                            }
                        )
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                except requests.RequestException as exc:
                    st.error(f"Could not connect to the backend: {exc}")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

        if st.button("← Back to home", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

    render_footer()


# ============================================================
# SIGNUP
# ============================================================


def signup_page():
    render_brand()

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown(
            """
            <div style="padding:2.2rem 1rem 0 0;">
                <div class="eyebrow">Get started</div>
                <h1 class="page-title" style="font-size:3rem;">Create your TutorRAG account.</h1>
                <div class="hero-copy">Choose your role and start building a smarter, document-based learning workflow.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if image_exists("signup.png"):
            st.image(asset_path("signup.png"), use_container_width=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### ✍️ Create account")
        st.markdown('<div class="muted-text">A few details and you are ready to go.</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        role = st.selectbox("I am a", ["Student", "Teacher"])

        with st.form("signup_form"):
            full_name = st.text_input("Full Name", placeholder="Your full name")
            email = st.text_input("Email", placeholder="you@example.com")
            username = st.text_input("Username", placeholder="Choose a username")
            password = st.text_input("Password", type="password", placeholder="Create a password")

            grade = None
            school = None
            if role == "Student":
                grade = st.number_input("Grade", 1, 12, value=1)
                school = st.text_input("School", placeholder="Your school")

            submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

            if submitted:
                endpoint = "/signup/student" if role == "Student" else "/signup/teacher"
                payload = {
                    "fullName": full_name,
                    "email": email,
                    "userName": username,
                    "password": password,
                }

                if role == "Student":
                    payload.update({"grade": grade, "school": school})

                try:
                    r = requests.post(
                        f"{BACKEND_URL}{endpoint}",
                        json=payload,
                        timeout=30,
                    )

                    if r.status_code == 200:
                        st.success("Account created successfully. You can now log in.")
                    else:
                        st.error(r.text)
                except requests.RequestException as exc:
                    st.error(f"Could not connect to the backend: {exc}")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

        if st.button("← Back to home", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

    render_footer()


# ============================================================
# SIDEBAR
# ============================================================


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">🎓 TutorRAG</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="profile-card">
                <div class="profile-name">{st.session_state.username}</div>
                <div class="profile-role">{st.session_state.role} · Grade {st.session_state.grade if st.session_state.role == 'Student' else '—'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.role == "Student":
            st.caption("LEARNING")
            if st.button("💬 Ask Questions", use_container_width=True):
                st.session_state.app_tab = "chat"
                st.rerun()
            if st.button("📝 Quiz Generator", use_container_width=True):
                st.session_state.app_tab = "quiz"
                st.rerun()
            if st.button("📜 Quiz History", use_container_width=True):
                st.session_state.app_tab = "history"
                st.rerun()
        else:
            st.caption("TEACHING")
            st.markdown('<div class="muted-text">Upload study material for students to use.</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.divider()

        if st.button("Logout", use_container_width=True):
            logout()


# ============================================================
# TEACHER DASHBOARD
# ============================================================


def teacher_dashboard():
    render_sidebar()

    st.markdown(
        """
        <div class="page-header">
            <div class="eyebrow">Teacher workspace</div>
            <div class="page-title">Upload study material</div>
            <div class="page-subtitle">Add PDF content and organize it by grade so students can learn from it.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        render_stat("Role", "Teacher")
    with c2:
        render_stat("Source", "PDF")
    with c3:
        render_stat("Pipeline", "RAG")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.25, 0.75], gap="large")

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### 📚 Add a document")
        st.markdown('<div class="muted-text">Upload a PDF containing the study material you want to make searchable.</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        pdf = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
        grade = st.number_input("Grade", 1, 12, value=1)

        if pdf:
            st.success(f"Selected: {pdf.name}")

        if st.button("Upload & index document", type="primary", disabled=not pdf, use_container_width=True):
            with st.spinner("Uploading and indexing..."):
                try:
                    files = {
                        "file": (
                            pdf.name,
                            BytesIO(pdf.getvalue()),
                            "application/pdf",
                        )
                    }
                    data = {"grade": str(int(grade))}
                    r = api("POST", "/upload_docs", files=files, data=data)

                    if r.status_code == 200:
                        st.success("Document uploaded and indexed successfully.")
                    else:
                        st.error(r.text)
                except (requests.RequestException, RuntimeError) as exc:
                    st.error(f"Upload failed: {exc}")

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="soft-panel">', unsafe_allow_html=True)
        st.markdown("### Why upload material?")
        st.markdown(
            """
            <div class="feature-copy">
                Once indexed, the material can be used by the student-facing RAG workflow for grounded questions and quiz generation.
            </div>
            <br>
            <div class="pill">📄 PDF</div>
            <div style="height:.45rem"></div>
            <div class="pill">🔎 Searchable</div>
            <div style="height:.45rem"></div>
            <div class="pill">🤖 AI-ready</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    render_footer()


# ============================================================
# STUDENT DASHBOARD
# ============================================================


def student_dashboard():
    render_sidebar()

    st.markdown(
        """
        <div class="page-header">
            <div class="eyebrow">Student workspace</div>
            <div class="page-title">Welcome back 👋</div>
            <div class="page-subtitle">Ask your documents, test yourself, and review your progress.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        render_stat("Grade", st.session_state.grade)
    with c2:
        render_stat("Mode", "RAG Tutor")
    with c3:
        history_count = len(st.session_state.quiz_history or [])
        render_stat("Loaded history", history_count)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    tab_names = ["💬 Ask Questions", "📝 Quiz Generator", "📜 Quiz History"]
    chat_tab, quiz_tab, history_tab = st.tabs(tab_names)

    # --------------------------------------------------------
    # CHAT
    # --------------------------------------------------------
    with chat_tab:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### 💬 Ask your AI tutor")
        st.markdown('<div class="muted-text">Questions are sent to your RAG backend so the answer can be grounded in your uploaded material.</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

        if not st.session_state.chat_messages:
            st.markdown(
                """
                <div class="empty-state">
                    <div class="empty-icon">🧠</div>
                    <div class="empty-title">Start a study conversation</div>
                    <div class="empty-copy">Ask for explanations, definitions, summaries, or help understanding a topic from your material.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        st.markdown('</div>', unsafe_allow_html=True)

        prompt = st.chat_input("Ask a question about your study material...")
        if prompt:
            st.session_state.chat_messages.append(
                {"role": "user", "content": prompt}
            )

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        r = api("POST", "/chat", json={"query": prompt})
                        if r.status_code == 200:
                            data = r.json()
                            answer = data["answer"]
                            if data.get("sources"):
                                answer += "\n\n**Sources:** " + ", ".join(data["sources"])

                            st.markdown(answer)
                            st.session_state.chat_messages.append(
                                {"role": "assistant", "content": answer}
                            )
                        else:
                            st.error(r.text)
                    except (requests.RequestException, RuntimeError) as exc:
                        st.error(f"Could not reach the backend: {exc}")

    # --------------------------------------------------------
    # QUIZ
    # --------------------------------------------------------
    with quiz_tab:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### 📝 Generate a quiz")
        st.markdown('<div class="muted-text">Choose a topic and let the backend generate questions from your learning workflow.</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

        if st.session_state.generated_quiz is None:
            topic = st.text_input("Quiz Topic", placeholder="e.g. Newton's Laws")
            num_q = st.slider("Number of Questions", 1, 10, 3)

            if st.button("Generate Quiz", type="primary", disabled=not topic, use_container_width=True):
                try:
                    with st.spinner("Generating quiz..."):
                        r = api(
                            "POST",
                            "/quiz",
                            json={"topic": topic, "num_questions": num_q},
                        )

                    if r.status_code == 200:
                        st.session_state.generated_quiz = r.json()
                        st.session_state.generated_quiz["topic"] = topic
                        st.session_state.quiz_result = None
                        st.rerun()
                    else:
                        st.error(r.text)
                except (requests.RequestException, RuntimeError) as exc:
                    st.error(f"Could not generate quiz: {exc}")
        else:
            quiz = st.session_state.generated_quiz
            questions = render_parsed_quiz(quiz["quiz"])

            st.markdown(
                f"<div class='pill'>Topic: {quiz.get('topic', 'Quiz')}</div>",
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)

            with st.form("quiz_form"):
                answers = []

                for i, question in enumerate(questions):
                    st.markdown(f"### Q{i + 1}. {question['q']}")
                    choice = st.radio(
                        "Choose an answer",
                        [option[0] for option in question["opts"]],
                        format_func=lambda x, opts=question["opts"]: next(
                            option for option in opts if option.startswith(x)
                        ),
                        key=f"quiz_q{i}",
                    )
                    answers.append(choice)
                    st.divider()

                submitted = st.form_submit_button("Submit Quiz", type="primary", use_container_width=True)

            if submitted:
                try:
                    r = api(
                        "POST",
                        "/quiz/check",
                        json={
                            "quiz_id": quiz["quiz_id"],
                            "answers": answers,
                        },
                    )

                    if r.status_code == 200:
                        st.session_state.quiz_result = r.json()
                        st.session_state.generated_quiz = None
                        st.rerun()
                    else:
                        st.error(r.text)
                except (requests.RequestException, RuntimeError) as exc:
                    st.error(f"Could not submit quiz: {exc}")

        if st.session_state.quiz_result:
            res = st.session_state.quiz_result
            st.success(res["message"])

            for result in res["results"]:
                status = "✅ Correct" if result["is_correct"] else "❌ Incorrect"
                st.markdown(
                    f"""
                    <div class="soft-panel" style="margin-bottom:.7rem;">
                        <div class="pill">Q{result['question_number']} · {status}</div>
                        <div style="margin-top:.6rem;" class="feature-copy">
                            Your answer: <strong>{result['user_answer']}</strong><br>
                            Correct answer: <strong>{result['correct_answer']}</strong>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if st.button("Start New Quiz", use_container_width=True):
                st.session_state.quiz_result = None
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------
    with history_tab:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("### 📜 Quiz history")
        st.markdown('<div class="muted-text">Load your previous attempts and review exactly where you got questions right or wrong.</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

        if st.button("Load History", type="primary", use_container_width=True):
            try:
                r = api("GET", "/quiz/history")
                if r.status_code == 200:
                    st.session_state.quiz_history = r.json()["history"]
                    st.rerun()
                else:
                    st.error(r.text)
            except (requests.RequestException, RuntimeError) as exc:
                st.error(f"Could not load history: {exc}")

        history = st.session_state.quiz_history

        if history:
            for attempt in history:
                score = attempt["score"]
                total = attempt["total"]
                percent = int((score / total) * 100) if total else 0

                with st.expander(f"{attempt['topic']}  ·  {score}/{total}  ·  {percent}%"):
                    st.progress(percent / 100)

                    parsed = render_parsed_quiz(attempt["quiz_content"])

                    for i, result in enumerate(attempt["results"]):
                        if i >= len(parsed):
                            break

                        question = parsed[i]
                        st.markdown(f"### Q{i + 1}: {question['q']}")

                        for option in question["opts"]:
                            letter = option[0]
                            if letter == result["correct_answer"]:
                                st.success(f"{option} · Correct")
                            elif letter == result["user_answer"]:
                                st.error(f"{option} · Your answer")
                            else:
                                st.write(option)

                        st.divider()
        else:
            st.markdown(
                """
                <div class="empty-state">
                    <div class="empty-icon">📜</div>
                    <div class="empty-title">No quiz history loaded</div>
                    <div class="empty-copy">Click “Load History” to fetch your previous attempts.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown('</div>', unsafe_allow_html=True)

    render_footer()


# ============================================================
# ROUTER
# ============================================================

if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "app":
    if st.session_state.role == "Teacher":
        teacher_dashboard()
    else:
        student_dashboard()

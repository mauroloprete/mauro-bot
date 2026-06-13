import os
import uuid

import streamlit as st
from databricks.sdk import WorkspaceClient

ENDPOINT = os.getenv("SERVING_ENDPOINT", "soporte-bot-dev")

st.set_page_config(page_title="SoporteBot", page_icon="./logo.svg", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Base */
    .stApp { background: #f8f9fb; font-family: 'Inter', sans-serif; }
    header[data-testid="stHeader"] { background: #1e293b; }
    .block-container { max-width: 720px; padding-top: 1.5rem; }

    /* Header card */
    .hero {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 16px;
        padding: 1.8rem 2rem 1.4rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 24px rgba(30,41,59,0.12);
    }
    .hero h1 {
        color: #FFA166; font-size: 1.7rem; font-weight: 700;
        margin: 0 0 0.25rem;
    }
    .hero p {
        color: #94a3b8; font-size: 0.92rem; margin: 0;
        line-height: 1.4;
    }
    .hero .badge {
        display: inline-block;
        background: rgba(255,161,102,0.15);
        color: #FFA166;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        margin-top: 0.6rem;
        letter-spacing: 0.03em;
    }

    /* Chat bubbles */
    [data-testid="stChatMessage"] {
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        background: white;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        margin-bottom: 0.6rem;
    }

    /* Input */
    [data-testid="stChatInput"] textarea {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #FFA166 !important;
        box-shadow: 0 0 0 3px rgba(255,161,102,0.15) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #1e293b;
    }
    [data-testid="stSidebar"] * { color: #cbd5e1; }
    [data-testid="stSidebar"] h2 { color: #FFA166; font-size: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header ---
st.markdown(
    """
    <div class="hero">
        <h1>SoporteBot</h1>
        <p>Base de conocimiento del equipo. Preguntame sobre procesos,
        documentación, o cualquier duda operativa.</p>
        <span class="badge">Databricks RAG + Lakebase</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## Acerca de")
    st.markdown(
        "Busco respuestas en la documentación interna "
        "y recuerdo el contexto de la conversación."
    )
    st.divider()
    if st.button("Nueva conversacion", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

# --- Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribi tu pregunta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en la documentacion..."):
            w = WorkspaceClient()
            response = w.serving_endpoints.query(
                name=ENDPOINT,
                messages=[{"role": "user", "content": prompt}],
                extra_params={"thread_id": st.session_state.thread_id},
            )
            answer = response.choices[0].message.content
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

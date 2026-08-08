import os
import sys
import threading

import streamlit as st
import uvicorn

from utils import get_image_base64, find_logo_path
from session import init_session_state
from styles import inject_global_css
from database import init_db
from components.landing import render_landing
from components.topbar import render_topbar
from components.sidebar import render_sidebar
from components.workspace import render_workspace

st.set_page_config(page_title="Readora AI", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
backend_dir = os.path.join(project_root, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app as fastapi_app  # noqa: E402  (matches main.py's own "app.*" scheme — avoids the backend.app vs app duplicate-import loop)


def _start_backend():
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000, log_level="warning")


if "backend_started" not in st.session_state:
    threading.Thread(target=_start_backend, daemon=True).start()
    st.session_state["backend_started"] = True

logo_path = find_logo_path(current_dir)
logo_b64 = get_image_base64(logo_path)
if logo_b64:
    logo_src = f"data:image/jpeg;base64,{logo_b64}"
else:
    logo_src = (
        "data:image/svg+xml;utf8,"
        "<svg xmlns='http://www.w3.org/2000/svg' width='45' height='45'>"
        "<rect width='45' height='45' rx='22.5' fill='%2300E5FF'/>"
        "<text x='50%25' y='58%25' font-family='sans-serif' font-size='20' "
        "fill='%230E1117' text-anchor='middle'>R</text></svg>"
    )

init_db()
init_session_state()
inject_global_css(logo_src)

if not st.session_state.logged_in:
    render_landing(logo_src)
else:
    render_topbar()
    render_sidebar()
    render_workspace()
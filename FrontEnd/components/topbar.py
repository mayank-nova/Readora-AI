import streamlit as st

def render_topbar():
    active_doc_name = st.session_state.get('last_uploaded_file')
    if active_doc_name:
        doc_status_val = (active_doc_name[:25] + '…') if len(active_doc_name) > 25 else active_doc_name
        doc_icon = "📄"
    else:
        doc_status_val = "None loaded yet"
        doc_icon = "📥"

    raw_name = st.session_state.username if st.session_state.get('username') else "Guest"
    display_name = raw_name.title()

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 5px 12px 5px; margin-bottom: 10px; border-bottom: 1px solid #2D303E;">
        <div>
            <h2 style="font-family: 'OpenDyslexic', 'Fraunces', Georgia, serif !important; font-size: 26px !important; font-weight: 700 !important; color: #E0E0E0 !important; margin: 0 !important;">
                Hello, {display_name}
            </h2>
        </div>
        <div style="display: flex; align-items: center; gap: 8px; background: #1A1C23; border: 1px solid #2D303E; border-radius: 6px; padding: 6px 12px;">
            <div style="font-size: 14px;">{doc_icon}</div>
            <div style="line-height: 1.1;">
                <div style="font-size: 9px; color: #6D7280; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">Current Document</div>
                <div style="font-size: 13px; color: #E0E0E0; font-weight: 600;">{doc_status_val}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
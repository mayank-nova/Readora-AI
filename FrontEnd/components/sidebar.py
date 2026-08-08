import base64
import streamlit as st
import streamlit.components.v1 as components
from database import get_user_documents, update_profile_photo

def handle_search():
    """Runs exactly when the user types a document name and hits Enter."""
    query = st.session_state.get("search_bar_input", "").lower()
    if query:
        user_history = get_user_documents(st.session_state.username)
        match = next((doc for doc in user_history if query in doc[1].lower()), None)
        
        if match:
            st.session_state.current_doc_id = match[0]
            st.session_state.last_uploaded_file = match[1]
            st.session_state.extracted_text = match[2]
            st.session_state.simplified_text = match[3]
            st.session_state.is_reading = False
            st.session_state.flash_doc_name = match[1]
        else:
            st.toast("No matching document found.", icon="⚠️")
    st.session_state.search_bar_input = ""

def render_sidebar():
    # 🚨 FIX: Changed the keys to force Streamlit to wipe its cache and apply 20 and 2.10!
    if 'ui_font_size' not in st.session_state:
        st.session_state.ui_font_size = 20
    if 'ui_line_spacing' not in st.session_state:
        st.session_state.ui_line_spacing = 2.10

    with st.sidebar:
        raw_name = st.session_state.username if st.session_state.get('username') else "Guest"
        display_name = raw_name.title()
        initial = display_name[0].upper()

        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 20px;">
            <div class="logo-dot" style="width:14px; height:14px; border-radius:50%; background: linear-gradient(135deg, #00E5FF, #69F0AE); flex-shrink:0;"></div>
            <span style="font-family:'OpenDyslexic', 'Fraunces', Georgia, serif; font-style: italic; font-weight:700; font-size:16px; color:#FFFFFF;">Readora AI</span>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.get('profile_photo'):
            b64_img = base64.b64encode(st.session_state.profile_photo).decode()
            avatar_html = f'<img src="data:image/jpeg;base64,{b64_img}" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover;">'
        else:
            avatar_html = f'<div style="width: 36px; height: 36px; border-radius: 50%; background-color: #00E5FF; color: #0E1117; display: flex; justify-content: center; align-items: center; font-weight: 700; font-size: 16px; flex-shrink:0;">{initial}</div>'

        popover_key = "My_Profile_Btn"
        with st.popover(popover_key, use_container_width=True):
            st.markdown(f"**⚙️ Account Settings: {display_name}**")
            
            if st.session_state.get('profile_photo'):
                if st.button("🗑️ Delete Photo", use_container_width=True):
                    st.session_state.profile_photo = None
                    update_profile_photo(st.session_state.username, None)
                    st.rerun()
            else:
                uploaded_img = st.file_uploader("Upload Profile Photo", type=["jpg", "png", "jpeg"])
                if uploaded_img:
                    photo_bytes = uploaded_img.getvalue()
                    st.session_state.profile_photo = photo_bytes
                    update_profile_photo(st.session_state.username, photo_bytes)
                    st.rerun()
            
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            if st.button("🚪 Log Out", use_container_width=True, type="primary"):
                st.session_state.logged_in = False
                st.rerun()

        # 🚨 FIX: We now target the exact Streamlit element ID, avoiding the text-matching bug.
        card_js = f"""
        <script>
            setTimeout(function() {{
                const doc = window.parent.document;
                // Finds the popover purely by its architecture, not its text!
                const sidebar = doc.querySelector('[data-testid="stSidebar"]');
                if (sidebar) {{
                    const btn = sidebar.querySelector('[data-testid="stPopover"] button');
                    if (btn) {{
                        btn.style.padding = "10px 14px";
                        btn.style.background = "rgba(255,255,255,0.03)";
                        btn.style.border = "1px solid #2D303E";
                        btn.style.borderRadius = "8px";
                        
                        btn.innerHTML = `<div style="display:flex; align-items:center; gap: 12px; width: 100%; text-align: left;">
                            {avatar_html}
                            <div style="line-height: 1.2; flex:1;">
                                <div style="font-weight: 600; color: #E0E0E0; font-size: 14px; font-family: 'Figtree', sans-serif;">{display_name}</div>
                                <div style="font-size: 11px; color: #00E5FF; margin-top: 2px; font-family: 'Figtree', sans-serif;">⚙️ Settings</div>
                            </div>
                        </div>`;
                    }}
                }}
            }}, 50);
        </script>
        """
        components.html(card_js, height=0)

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        st.text_input("Search", placeholder="🔍 Search documents...", key="search_bar_input", on_change=handle_search, label_visibility="collapsed")

        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        if st.button("✨ New Chat", use_container_width=True, type="primary"):
            st.session_state.extracted_text = ""
            st.session_state.simplified_text = ""
            st.session_state.last_uploaded_file = None
            st.session_state.current_doc_id = None
            st.session_state.is_reading = False
            st.rerun()

        st.markdown("<span class='sb-section-label'>Recent Documents</span>", unsafe_allow_html=True)

        user_history = get_user_documents(st.session_state.username)

        with st.container(height=450):
            if not user_history:
                st.markdown("<span style='color: #5A5E73; font-size: 0.8rem;'>No documents yet.</span>", unsafe_allow_html=True)
            else:
                for doc in user_history:
                    doc_id, doc_name, orig_text, simp_text = doc
                    display_name_doc = (doc_name[:22] + '…') if len(doc_name) > 22 else doc_name
                    is_active = st.session_state.get('current_doc_id') == doc_id
                    icon = "🟢" if is_active else "📄"
                    
                    if st.button(f"{icon} {display_name_doc}", key=f"hist_{doc_id}", use_container_width=True):
                        st.session_state.current_doc_id = doc_id
                        st.session_state.last_uploaded_file = doc_name
                        st.session_state.extracted_text = orig_text
                        st.session_state.simplified_text = simp_text
                        st.session_state.is_reading = False
                        st.rerun()

                    if st.session_state.get('flash_doc_name') == doc_name:
                        flash_js = f"""
                        <script>
                            setTimeout(() => {{
                                const btns = window.parent.document.querySelectorAll('button');
                                btns.forEach(b => {{
                                    if(b.innerText.includes("{display_name_doc}")) {{
                                        b.style.transition = "all 0.5s ease";
                                        b.style.backgroundColor = "#00E5FF";
                                        b.style.color = "#000";
                                        b.style.transform = "scale(1.05)";
                                        setTimeout(() => {{
                                            b.style.backgroundColor = "";
                                            b.style.color = "";
                                            b.style.transform = "";
                                        }}, 1500);
                                    }}
                                }});
                            }}, 100);
                        </script>
                        """
                        components.html(flash_js, height=0)
                        st.session_state.flash_doc_name = None 

        with st.expander("🔤 Visual Settings", expanded=False):
            # 🚨 FIX: Now uses the new UI keys so Streamlit is forced to use the new defaults
            st.slider("Font Size", 16, 40, key='ui_font_size')
            st.slider("Line Spacing", 1.0, 4.0, step=0.10, key='ui_line_spacing')
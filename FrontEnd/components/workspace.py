import markdown
import time
import streamlit as st
import streamlit.components.v1 as components

from config import BACKEND_URL
from api_client import upload_pdf, simplify_text_request
from database import insert_document, update_document_simplified
from styles import inject_workspace_css, inject_reading_pane_size_css
from components.reader import build_reader_html

def render_workspace():
    if st.session_state.get('stop_audio'):
        components.html("<script>window.parent.speechSynthesis.cancel();</script>", height=0)
        st.session_state.stop_audio = False

    if st.session_state.get('scroll_to_top'):
        scroll_js = """
        <script>
            setTimeout(function() {
                const p = window.parent.document;
                p.querySelectorAll('.stAppViewContainer, .main, [data-testid="stMainContainer"], .stApp').forEach(el => el.scrollTo(0,0));
                window.parent.scrollTo(0,0);
            }, 100);
        </script>
        """
        st.markdown(scroll_js, unsafe_allow_html=True)
        st.session_state.scroll_to_top = False

    inject_workspace_css()

    _, center_col, _ = st.columns([1, 3, 1])
    
    with center_col:
        uploaded_file = st.file_uploader("Drop your reading material here (PDF)", type=['pdf'], label_visibility="collapsed")

        if uploaded_file is not None:
            if st.session_state.get('last_uploaded_file') != uploaded_file.name:
                status_placeholder = st.empty()
                status_placeholder.info("⏳ Uploading & Extracting... (Photo PDFs may take up to 10-15 seconds. Please wait.)")
                
                start_time = time.time()
                try:
                    response = upload_pdf(uploaded_file.name, uploaded_file.getvalue())
                    elapsed = round(time.time() - start_time, 2)
                    status_placeholder.empty()

                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.extracted_text = data.get("text", "")
                        st.session_state.last_uploaded_file = uploaded_file.name
                        st.session_state.simplified_text = ""
                        st.session_state.vocabulary = ""

                        doc_id = insert_document(
                            st.session_state.username, uploaded_file.name, st.session_state.extracted_text, ""
                        )
                        st.session_state.current_doc_id = doc_id
                        st.success(f"✅ Document extracted successfully in {elapsed} seconds!")
                    else:
                        st.error(f"Upload Error: {response.json().get('detail')}")
                except Exception as e:
                    status_placeholder.empty()
                    st.error(f"Connection Error: Could not connect to FastAPI backend on {BACKEND_URL}")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        btn1, btn2 = st.columns(2)
        with btn1:
            btn_simplify = st.button("✨ Simplify", type="primary", use_container_width=True)
        with btn2:
            read_btn_label = "⏹ Stop" if st.session_state.get('is_reading') else "🔊 Read Aloud"
            btn_read = st.button(read_btn_label, use_container_width=True)

        if btn_read:
            if st.session_state.get('is_reading'):
                st.session_state.is_reading = False
                st.session_state.stop_audio = True 
            else:
                if st.session_state.simplified_text:
                    st.session_state.is_reading = True
                else:
                    st.warning("Generate the AI-simplified version first (click '✨ Simplify').")
            st.rerun()

        if btn_simplify:
            if st.session_state.extracted_text and st.session_state.extracted_text.strip():
                with st.spinner("Readora AI is breaking down complex concepts..."):
                    start_time = time.time()
                    try:
                        response = simplify_text_request(st.session_state.extracted_text)
                        elapsed = round(time.time() - start_time, 2)

                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.simplified_text = data.get("simplified_text", "")
                            st.session_state.vocabulary = data.get("vocabulary", "")

                            if st.session_state.current_doc_id:
                                update_document_simplified(st.session_state.current_doc_id, st.session_state.simplified_text)

                            st.toast(f"Text simplified in {elapsed} seconds!", icon="✨")
                            st.rerun()
                        else:
                            st.error(f"Simplification Error: {response.json().get('detail')}")
                    except Exception as e:
                        st.error(f"Connection Error: Could not connect to FastAPI backend on {BACKEND_URL}")
            elif uploaded_file is not None:
                st.warning("⚠️ The PDF uploaded, but the backend couldn't extract any words.")
            else:
                st.warning("Please upload a PDF document first!")

        word_count = len(st.session_state.extracted_text.split()) if st.session_state.extracted_text else 0
        simplified_ready = bool(st.session_state.simplified_text)
        
        st.markdown(f"""
        <div style="display: flex; flex-direction: row; gap: 15px; justify-content: center; align-items: center; margin: 15px 0;">
            <div style="background: rgba(30, 28, 41, 0.7); border: 1px solid #2D303E; border-radius: 6px; padding: 6px 12px; font-size: 13px; color: #9AA0A6;">
                📄 <b>{word_count:,}</b> words extracted
            </div>
            <div style="background: rgba(30, 28, 41, 0.7); border: 1px solid #2D303E; border-radius: 6px; padding: 6px 12px; font-size: 13px; color: #9AA0A6;">
                ✨ Simplified: <b style="color: #00E5FF;">{"Ready" if simplified_ready else "Not yet"}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 🚨 FIX: Pointed to our new, forced-reset visual setting keys!
    inject_reading_pane_size_css(st.session_state.get('ui_font_size', 20), st.session_state.get('ui_line_spacing', 2.10))
    custom_text_style = ""

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["✨ AI Simplified", "📚 Key Vocabulary", "📄 Original PDF Text"])

    with tab1:
        st.markdown('<div class="reading-container">', unsafe_allow_html=True)
        if st.session_state.simplified_text:
            if st.session_state.get('is_reading'):
                st.iframe(build_reader_html(st.session_state.simplified_text), height=250)
            else:
                st.markdown('<div class="badge">AI Output</div>', unsafe_allow_html=True)
                parsed_html = markdown.markdown(st.session_state.simplified_text)
                st.markdown(f'<div class="reading-pane" style="{custom_text_style}">{parsed_html}</div>', unsafe_allow_html=True)
        else:
            st.info("Upload a PDF and click '✨ Simplify' to generate a neurodivergent-friendly version.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="reading-container">', unsafe_allow_html=True)
        if st.session_state.get('vocabulary'):
            st.markdown('<div class="badge">Vocabulary List</div>', unsafe_allow_html=True)
            parsed_vocab_html = markdown.markdown(st.session_state.vocabulary)
            st.markdown(f'<div class="reading-pane" style="{custom_text_style}">{parsed_vocab_html}</div>', unsafe_allow_html=True)
        else:
            st.info("Click '✨ Simplify' to generate a vocabulary breakdown.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="reading-container">', unsafe_allow_html=True)
        if st.session_state.extracted_text:
            st.markdown('<div class="badge">Raw Extraction</div>', unsafe_allow_html=True)
            parsed_raw_html = markdown.markdown(st.session_state.extracted_text)
            st.markdown(f'<div class="reading-pane" style="{custom_text_style}">{parsed_raw_html}</div>', unsafe_allow_html=True)
        else:
            st.info("Your original document text will appear here.")
        st.markdown('</div>', unsafe_allow_html=True)
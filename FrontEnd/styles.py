import streamlit as st

from config import (
    bg_color, text_color, card_color, cyan_color, accent_color, border_color,
    paper_bg, paper_ink, paper_border, paper_accent,
)


def inject_global_css(logo_src):
    """The full app stylesheet."""
    dynamic_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Figtree:wght@400;500;600;700&display=swap');

#MainMenu {{visibility: hidden !important;}}
footer {{visibility: hidden !important;}}

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMainContainer"], [data-testid="stMain"] {{
    scroll-behavior: smooth !important;
}}

@font-face {{
    font-family: 'OpenDyslexic';
    src: url('https://cdn.jsdelivr.net/gh/antijingoist/opendyslexic@master/compiled/OpenDyslexic-Regular.otf') format('opentype');
    font-weight: normal;
    font-style: normal;
}}

.stApp {{ background-color: {bg_color}; }}

html, body, [class*="css"], p, li, label, .stMarkdown {{
    font-family: 'OpenDyslexic', 'Figtree', sans-serif !important;
    color: {text_color} !important;
}}
h1, h2, h3, h4, h5, h6, .nav-title, .hero-text-light, .hero-text-cyan {{
    font-family: 'OpenDyslexic', 'Fraunces', Georgia, serif !important;
    font-weight: 700 !important;
    color: {text_color} !important;
}}


/* ======================================================================
   SECTION 1: THE HERO PAGE (Kept identical for exact wrapping)
   ====================================================================== */

.hero-wrapper {{ padding: 2.5rem 0 1.5rem 0; margin-top: 40px; text-align: center; position: relative; overflow: hidden; }}

.hero-eyebrow {{
    font-family: 'OpenDyslexic', 'Figtree', sans-serif; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.14em;
    text-transform: uppercase; color: {accent_color}; margin-bottom: 10px;
}}
.hero-copy h1 {{
    font-family: 'OpenDyslexic', 'Fraunces', Georgia, serif !important; 
    font-size: 2.05rem !important; 
    line-height: 1.15;
    font-weight: 600 !important; margin: 0 0 14px 0 !important; color: {text_color} !important; text-align: left;
}}
.hero-copy h1 em {{ font-style: italic; color: {cyan_color}; font-weight: 700; }}
.hero-copy p {{ font-size: 1rem; color: #9AA0A6 !important; max-width: 430px; margin-bottom: 20px !important; text-align: left; line-height: 1.6; }}

.cta-btn {{
    display: inline-block; background-color: {cyan_color}; color: #0E1117 !important; text-decoration: none !important;
    font-family: 'OpenDyslexic', 'Figtree', sans-serif; font-weight: 700; font-size: 0.95rem; padding: 10px 22px; border-radius: 6px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.cta-btn:hover {{ transform: translateY(-2px); box-shadow: 0 5px 14px rgba(0,229,255,0.3); }}
.cta-sub {{ font-size: 0.8rem; color: #6D6558; margin-top: 8px; }}

.stack-wrap {{ position: relative; height: 280px; }}
.stack-back {{
    position: absolute; top: 10px; left: 25px; width: 78%; padding: 20px 24px; border-radius: 8px;
    background-color: {card_color}; border: 1px solid {border_color}; transform: rotate(-7deg);
    box-shadow: 0 8px 16px rgba(0,0,0,0.35); opacity: 0.7;
}}
.stack-back p {{ font-family: 'Arial', sans-serif !important; font-size: 0.8rem !important; line-height: 1.6 !important; color: #857D6E !important; margin: 0 !important; }}
.stack-back .stack-label {{ font-family: 'OpenDyslexic', 'Figtree', sans-serif; font-size: 0.65rem; font-weight: 700; color: #6D6558; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; display: block; }}
.stack-front {{
    position: absolute; top: 35px; left: 0; width: 82%; padding: 24px 28px; border-radius: 5px 12px 12px 5px;
    background-color: {paper_bg}; border: 1px solid {paper_border}; transform: rotate(3deg);
    box-shadow: 0 14px 26px rgba(0,0,0,0.45);
}}
.stack-front::after {{
    content: ''; position: absolute; top: 0; right: 0; width: 0; height: 0;
    border-style: solid; border-width: 0 16px 16px 0; border-color: transparent #DCCEA4 transparent transparent;
}}
.stack-front .stack-label {{ font-family: 'OpenDyslexic', 'Figtree', sans-serif; font-size: 0.65rem; font-weight: 700; color: {paper_accent}; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; display: block; }}
.stack-front p {{ font-family: 'OpenDyslexic', sans-serif !important; font-size: 0.9rem !important; line-height: 1.75 !important; color: {paper_ink} !important; margin: 0 !important; }}
.stack-pill {{
    position: absolute; bottom: 12px; right: 6%; background-color: {accent_color}; color: #0E1117;
    font-family: 'OpenDyslexic', 'Figtree', sans-serif; font-weight: 700; font-size: 0.75rem; padding: 5px 12px;
    border-radius: 15px; box-shadow: 0 5px 12px rgba(0,0,0,0.35); z-index: 5;
}}


/* ======================================================================
   SECTION 2: FEATURES PAGE (Enlarged +10%)
   ====================================================================== */

.features-heading {{
    font-family: 'OpenDyslexic', 'Fraunces', Georgia, serif !important;
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: 10px;
    color: {text_color};
}}
.features-subtext {{
    font-size: 1.2rem;
    color: #9AA0A6;
    margin-bottom: 30px;
}}

.feature-grid {{ display: flex; gap: 18px; margin-top: 10px; }}
.feature-card {{
    flex: 1; background-color: {card_color}; border: 1px solid {border_color}; border-left: 2px solid var(--accent, {cyan_color});
    border-radius: 10px; padding: 26px 22px; transition: transform 0.2s ease, border-color 0.2s ease;
}}
.feature-card:hover {{ transform: translateY(-3px); }}
.feature-icon {{
    width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; background-color: rgba(255,255,255,0.06); margin-bottom: 15px;
}}
.feature-card h4 {{ font-family: 'OpenDyslexic', 'Fraunces', Georgia, serif !important; font-size: 1.25rem; margin: 0 0 8px 0 !important; color: {text_color} !important; }}
.feature-card p {{ font-size: 1.05rem; color: #9AA0A6 !important; margin: 0 !important; line-height: 1.6; }}


/* ======================================================================
   SECTION 3: LOGIN PAGE & FOOTER (Enlarged +10%)
   ====================================================================== */

.auth-card-header {{ text-align: center; margin-bottom: 22px; }}
.auth-card-header .icon-badge {{
    width: 54px; height: 54px; border-radius: 50%; background-color: rgba(0,229,255,0.12); border: 1px solid {cyan_color};
    display: flex; align-items: center; justify-content: center; margin: 0 auto 14px auto; overflow: hidden;
}}
.auth-card-header h3 {{ margin: 0 0 6px 0 !important; font-size: 1.75rem !important; font-weight: 700 !important; }}
.auth-card-header p {{ color: #9AA0A6 !important; font-size: 1.05rem; margin: 0 !important; }}

div[class*="st-key-auth_card"] {{
    background-color: {card_color} !important;
    border: 1px solid {border_color} !important;
    border-radius: 14px !important;
    padding: 34px 40px 28px 40px !important;
    box-shadow: 0 12px 24px rgba(0,0,0,0.4);
}}

.mega-footer {{
    display: flex; justify-content: space-around; background-color: {card_color}; padding: 40px 24px; border-top: 1px solid {border_color};
    margin-top: 60px; border-radius: 12px;
}}
.footer-col {{ display: flex; flex-direction: column; text-align: left; }}
.footer-col h4 {{ color: #FFFFFF !important; font-size: 1.05rem; margin-bottom: 12px; font-weight: 600; font-family: 'OpenDyslexic', 'Figtree', sans-serif !important;}}
.footer-col a {{ color: #9AA0A6 !important; text-decoration: none; font-size: 0.95rem; margin-bottom: 8px; transition: color 0.2s, transform 0.2s; }}
.footer-col a:hover {{ color: {cyan_color} !important; transform: translateX(3px); }}


/* ======================================================================
   WORKSPACE COMPONENTS (Untouched, kept accessible)
   ====================================================================== */

[data-testid="stUploadedFile"] {{ border: 1px solid #5A5E73 !important; border-radius: 6px !important; background-color: #222530 !important; }}
[data-testid="stAlert"] {{ background-color: rgba(105, 240, 174, 0.15) !important; border: 1px solid {accent_color} !important; color: #FFFFFF !important; }}

[data-testid="stMain"] .block-container {{
    padding-top: 40px !important; 
    padding-bottom: 15px !important;
}}
[data-testid="stMain"] {{ background-color: {bg_color}; }}

[data-testid="stSidebar"] {{ background-color: #13151C !important; border-right: 1px solid {border_color}; }}
[data-testid="stSidebar"] button[kind="secondary"] {{
    background-color: transparent !important; border: none !important; justify-content: flex-start !important; 
    padding: 6px 8px !important; box-shadow: none !important;
    border-radius: 5px !important; margin-bottom: 3px !important;
}}
[data-testid="stSidebar"] button[kind="secondary"]:hover {{ background-color: #1E212B !important; }}

[data-testid="collapsedControl"] svg {{ display: none !important; }}
[data-testid="collapsedControl"] {{
    background-image: url('{logo_src}');
    background-size: cover; background-position: center; border-radius: 50%;
    width: 32px !important; height: 32px !important; border: 1px solid {cyan_color};
    margin-top: 8px; margin-left: 12px; transition: transform 0.2s ease; z-index: 999999 !important;
}}
[data-testid="collapsedControl"]:hover {{ transform: scale(1.1); }}

.stTabs [data-baseweb="tab-list"] {{ gap: 6px; background-color: transparent; }}
.stTabs [data-baseweb="tab"] {{ background-color: rgba(30, 28, 41, 0.7); border-radius: 6px 6px 0 0; color: #8b949e; padding: 8px 14px; border: 1px solid {border_color}; font-size: 0.9rem; }}
.stTabs [aria-selected="true"] {{ background-color: rgba(0, 229, 255, 0.12) !important; color: {cyan_color} !important; border-color: rgba(0, 229, 255, 0.4) !important; }}

.reading-pane {{
    position: relative; background-color: {paper_bg}; padding: 25px 40px; border-radius: 5px 8px 8px 5px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.35), inset 0 0 0 1px {paper_border}; border: 1px solid {paper_border}; transition: all 0.3s ease;
}}
.reading-pane::after {{
    content: ''; position: absolute; top: 0; right: 0; width: 0; height: 0; border-style: solid;
    border-width: 0 16px 16px 0; border-color: transparent #DCCEA4 transparent transparent;
    filter: drop-shadow(-1px 1px 3px rgba(0,0,0,0.18)); border-top-right-radius: 5px;
}}

.stButton button {{ white-space: nowrap !important; }}
button[kind="primary"] {{
    background-color: {cyan_color} !important; border: none !important; font-weight: 600 !important; font-size: 0.9rem !important;
    padding: 8px 16px !important; transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
button[kind="primary"] * {{ color: #0E1117 !important; }}
button[kind="primary"]:hover {{
    background-color: {accent_color} !important; transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0, 229, 255, 0.25);
}}

</style>
"""
    st.markdown(dynamic_css, unsafe_allow_html=True)


def inject_workspace_css():
    """Workspace-wide readability tweaks applied on top of the base font."""
    st.markdown("""
    <style>
    .stApp *:not([data-testid="stIconMaterial"]):not([class*="material-icons"]):not([class*="material-symbols"]),
    .stApp { font-family: 'OpenDyslexic', 'Figtree', sans-serif !important; }

    [data-testid="stTextInput"] input { font-size: 14px !important; padding-top: 6px !important; padding-bottom: 6px !important; }
    [data-testid="stTextInput"] input::placeholder { font-size: 14px !important; }
    
    [data-testid="stSidebar"] [data-testid="stTextInput"] input,
    [data-testid="stSidebar"] [data-testid="stTextInput"] input::placeholder { font-size: 13px !important; padding-top: 4px !important; padding-bottom: 4px !important; }

    .stApp p, .stApp li, .stApp label, .stApp span, .stApp div, [data-testid="stMarkdownContainer"] p {
        letter-spacing: 0.01em; line-height: 1.65 !important;
    }
    .stApp label, [data-testid="stWidgetLabel"] p { font-size: 13px !important; }
    [data-testid="stSidebar"] button p { font-size: 13px !important; }
    </style>
    """, unsafe_allow_html=True)


def inject_reading_pane_size_css(font_size, line_spacing):
    st.markdown(f"""
    <style>
        .reading-pane, .reading-pane p, .reading-pane li, .reading-pane span {{
            font-size: {font_size}px !important;
            line-height: {line_spacing} !important;
        }}
    </style>
    """, unsafe_allow_html=True)
import streamlit as st
from database import verify_user, create_user, get_profile_photo

def render_landing(logo_src):
    # Anchor the background strictly to the top section and fade it to solid #0E1117 at the bottom edge
    st.markdown(f"""
        <style>
            #smooth-logo-bg {{
                position: absolute;
                top: -150px; /* 🚨 CHANGED: Pulled way further up so the book and tree rise higher */
                left: 50%;
                transform: translateX(-50%);
                width: 100vw;
                height: 1000px; /* 🚨 CHANGED: Made taller to compensate for pulling it up */
                background: linear-gradient(to bottom, rgba(14, 17, 23, 0.45) 0%, #0E1117 95%), url('{logo_src}');
                background-size: cover;
                background-position: center center; /* 🚨 CHANGED: Centers the image rather than pinning to the top edge */
                pointer-events: none;
                z-index: 0;
            }}
        </style>
        
        <div id="smooth-logo-bg"></div>
    """, unsafe_allow_html=True)

    top_bar_container = st.container()
    with top_bar_container:
        st.markdown(f"""
            <style>
                .custom-top-bar {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 60px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 0 40px;
                    background-color: rgba(14, 17, 23, 0.45);
                    backdrop-filter: blur(16px);
                    -webkit-backdrop-filter: blur(16px);
                    border-bottom: 1px solid rgba(51, 47, 63, 0.4);
                    box-shadow: 0 2px 18px rgba(0, 0, 0, 0.15);
                    z-index: 999999;
                }}
                .nav-left-side {{
                    display: flex;
                    align-items: center;
                }}
                .nav-brand-title {{
                    font-family: 'OpenDyslexic', 'Fraunces', Georgia, serif;
                    font-size: 1.5rem;
                    font-weight: 700;
                    font-style: italic;
                    letter-spacing: 0.5px;
                    background: linear-gradient(135deg, #FFFFFF 30%, #00E5FF 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }}
                .nav-login-link {{
                    background-color: transparent;
                    color: #00E5FF !important;
                    border: 1.5px solid #00E5FF;
                    padding: 6px 18px;
                    border-radius: 25px;
                    text-decoration: none !important;
                    font-family: 'OpenDyslexic', 'Figtree', sans-serif;
                    font-size: 0.85rem;
                    font-weight: 600;
                    transition: all 0.25s ease;
                }}
                .nav-login-link:hover {{
                    background-color: #00E5FF;
                    color: #0E1117 !important;
                    box-shadow: 0 0 15px rgba(0, 229, 255, 0.5);
                    transform: translateY(-2px);
                }}
            </style>
            <div class="custom-top-bar">
                <div class="nav-left-side">
                    <span class="nav-brand-title">Readora AI</span>
                </div>
                <div>
                    <a href="#login-section" class="nav-login-link">Log In</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='height: 70px;'></div>", unsafe_allow_html=True)

    # --- PAGE 1: HERO SECTION ---
    hero_col1, hero_col2 = st.columns([1.05, 1], gap="medium")
    with hero_col1:
        st.markdown("""
        <div class="hero-copy">
            <div class="hero-eyebrow">For dyslexic, ADHD &amp; neurodivergent readers</div>
            <h1>Your brain isn't behind the AI curve.<br>It's been <em>ahead</em> of it for years.</h1>
            <p>Readora rewrites dense, academic text into short, plain-language sentences — set in a dyslexia-friendly typeface, at your pace, with your spacing.</p>
            <a href="#login-section" class="cta-btn">Try the live demo →</a>
            <div class="cta-sub">No credit card. Two minutes to your first simplified page.</div>
        </div>
        """, unsafe_allow_html=True)

    with hero_col2:
        st.markdown("""
        <div class="stack-wrap">
            <div class="stack-back">
                <span class="stack-label">Original textbook</span>
                <p>Photosynthesis is a process used by plants and other organisms to convert light energy into chemical energy that, through cellular respiration, can later be released to fuel the organism's activities.</p>
            </div>
            <div class="stack-front">
                <span class="stack-label">Readora</span>
                <p>Plants use sunlight to make their own food.<br><br>They store it as sugar, then use it later to grow.</p>
            </div>
            <div class="stack-pill">✨ Simplified in 4s</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # --- PAGE 2: FEATURES SECTION ---
    st.markdown("<h2 class='features-heading'>Built for neurodivergent minds</h2>", unsafe_allow_html=True)
    st.markdown("<p class='features-subtext'>Three things happen to your document the moment it lands in Readora.</p>", unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card" style="--accent: #00E5FF; border-left-color: #00E5FF;">
            <div class="feature-icon" style="color:#00E5FF;">📄</div>
            <h4>Reads how you read</h4>
            <p>OpenDyslexic type, wide letter spacing, and adjustable line height replace the dense default layout of the source PDF.</p>
        </div>
        <div class="feature-card" style="--accent: #B5651D; border-left-color: #B5651D;">
            <div class="feature-icon" style="color:#B5651D;">✨</div>
            <h4>Rewrites the concepts</h4>
            <p>Abstract, jargon-heavy paragraphs are broken into short, literal sentences — with a plain-language vocabulary list alongside.</p>
        </div>
        <div class="feature-card" style="--accent: #69F0AE; border-left-color: #69F0AE;">
            <div class="feature-icon" style="color:#69F0AE;">🔊</div>
            <h4>Reads it out loud</h4>
            <p>Word-by-word highlighted narration for anyone who processes audio and text together better than text alone.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    # --- PAGE 3: LOGIN SECTION ---
    st.markdown('<div id="login-section" style="padding-top: 50px; margin-top: -50px;"></div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    _, auth_col, _ = st.columns([1, 1.1, 1])
    with auth_col:
        with st.container(border=True, key="auth_card"):
            st.markdown(f"""
            <div class="auth-card-header">
                <div class="icon-badge"><img src="{logo_src}" alt="Readora AI" style="width:100%; height:100%; object-fit:cover;"></div>
                <h3>Access the app</h3>
                <p>Log in to pick up where you left off, or create an account.</p>
            </div>
            """, unsafe_allow_html=True)

            log_user = st.text_input("Username")
            log_pass = st.text_input("Password", type="password")
        
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Log In", type="primary", use_container_width=True):
                    if verify_user(log_user, log_pass):
                        st.session_state.logged_in = True
                        st.session_state.username = log_user
                        st.session_state.scroll_to_top = True
                        
                        # 🚨 THE FIX: Fetches their saved photo instantly on login
                        st.session_state.profile_photo = get_profile_photo(log_user) 
                        
                        st.rerun()
                    else:
                        st.toast("Invalid credentials. Please try again.", icon="🚨")
                        
            with c2:
                if st.button("Sign Up", use_container_width=True):
                    if log_user and log_pass:
                        create_user(log_user, log_pass)
                        st.toast("Account created! You can now log in.", icon="✅")
            
            st.markdown("<div style='text-align: center; margin: 16px 0; color: #5A5E73; font-size: 0.85rem;'>OR</div>", unsafe_allow_html=True)
        
            if st.button("🌐 Continue with Google", use_container_width=True):
                st.toast("Google OAuth integration coming soon!", icon="ℹ️")

    footer_html = """
    <div class="mega-footer">
        <div class="footer-col">
            <h4>Get to Know Us</h4>
            <a href="#">About Readora AI</a>
            <a href="#">Our Team at NSUT</a>
            <a href="#">Hackathon Mission</a>
            <a href="#">Press Releases</a>
        </div>
        <div class="footer-col">
            <h4>Connect with Us</h4>
            <a href="#">GitHub Repository</a>
            <a href="#">Twitter / X</a>
            <a href="#">Instagram</a>
            <a href="#">LinkedIn</a>
        </div>
        <div class="footer-col">
            <h4>Resources</h4>
            <a href="#">Dyslexia Support</a>
            <a href="#">ADHD Tools</a>
            <a href="#">Accessibility Guide</a>
            <a href="#">API Documentation</a>
        </div>
        <div class="footer-col">
            <h4>Legal & Help</h4>
            <a href="#">Your Account</a>
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
            <a href="#">Help Center</a>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
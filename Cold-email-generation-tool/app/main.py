import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import time
from datetime import datetime
import json
import os

# Configure the page with a professional theme
st.set_page_config(
    layout="wide",
    page_title="Cold Email Generator | Professional Outreach",
    page_icon="🚀",
    initial_sidebar_state="expanded"  # Changed to expanded for better navigation visibility
)


# Custom CSS for stunning animations and professional design
def inject_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main container styling */
    .main {
        padding: 0;
        max-width: 100%;
        animation: fadeIn 0.5s ease-in;
    }

    /* Navigation Bar Styling */
    .nav-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 2rem;
        margin: -3rem -3rem 2rem -3rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: sticky;
        top: 0;
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .nav-buttons {
        display: flex;
        gap: 1rem;
    }

    .nav-button {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 0.7rem 1.5rem;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 2px solid rgba(255,255,255,0.3);
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    .nav-button:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    .nav-button.active {
        background: white;
        color: #667eea;
    }

    .nav-logo {
        color: white;
        font-size: 1.5rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Hero Section Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes glow {
        0% { box-shadow: 0 0 20px rgba(79, 70, 229, 0.3); }
        50% { box-shadow: 0 0 40px rgba(79, 70, 229, 0.5); }
        100% { box-shadow: 0 0 20px rgba(79, 70, 229, 0.3); }
    }

    /* Hero gradient background */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #667eea 75%, #764ba2 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        padding: 4rem 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }

    /* Title styling */
    .main-title {
        color: white;
        font-size: 4rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        animation: slideInLeft 0.8s ease;
    }

    .subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 2rem;
        animation: slideInLeft 1s ease;
    }

    /* Stats cards */
    .stats-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
        animation: fadeIn 1.2s ease;
    }

    .stat-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        min-width: 150px;
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        background: rgba(255,255,255,0.15);
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
    }

    .stat-label {
        color: rgba(255,255,255,0.9);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* Input section styling */
    .input-section {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        margin: 2rem 0;
        animation: fadeIn 0.8s ease;
    }

    /* URL input field - FIXED TEXT COLOR */
    .stTextInput > div > div > input {
        font-size: 1.1rem;
        padding: 1rem;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        transition: all 0.3s ease;
        background: #f9fafb !important;
        color: #1a1a2e !important;  /* Dark text color */
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background: white !important;
        color: #1a1a2e !important;  /* Ensure text stays dark */
    }

    /* Fix for all text inputs including settings page */
    input[type="text"], input[type="email"], input[type="url"] {
        color: #1a1a2e !important;
        background: #f9fafb !important;
    }

    input[type="text"]:focus, input[type="email"]:focus, input[type="url"]:focus {
        color: #1a1a2e !important;
        background: white !important;
    }

    /* Fix for text areas */
    .stTextArea > div > div > textarea {
        color: #1a1a2e !important;
        background: #f9fafb !important;
    }

    /* Submit button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 1rem 3rem;
        border: none;
        border-radius: 12px;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        animation: pulse 2s infinite;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        animation: none;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Settings page card styling */
    .settings-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
    }

    .settings-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .required-field {
        color: #ef4444;
        font-size: 0.9rem;
        margin-left: 0.3rem;
    }

    .optional-badge {
        background: #e5e7eb;
        color: #6b7280;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }

    /* Social links section */
    .social-links-container {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
    }

    /* Result section */
    .result-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        animation: fadeIn 0.5s ease;
    }

    /* Code block styling */
    .stCodeBlock {
        animation: slideInLeft 0.6s ease;
    }

    .stCodeBlock > div {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        animation: glow 3s ease infinite;
    }

    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: #0f5132;
        padding: 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        text-align: center;
        margin: 1rem 0;
        animation: slideInLeft 0.5s ease;
    }

    /* Error styling */
    .stAlert {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffd93d 100%);
        border: none;
        border-radius: 12px;
        animation: shake 0.5s ease;
    }

    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }

    /* Loading animation */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem;
    }

    .spinner {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(102, 126, 234, 0.1);
        border-top: 4px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Features grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }

    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border-top: 4px solid transparent;
        border-image: linear-gradient(135deg, #667eea, #764ba2);
        border-image-slice: 1;
    }

    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
    }

    .feature-description {
        color: #6b7280;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)


def create_navigation_bar():
    """Create a custom navigation bar with Home and Settings buttons"""
    current_page = st.session_state.get('page', 'home')

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 2rem;">🚀</span>
            <span style="font-size: 1.5rem; font-weight: 800; color: #667eea;">Email Generator Pro</span>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button("🏠 Home", use_container_width=True, type="primary" if current_page == 'home' else "secondary"):
                st.session_state.page = 'home'
                st.rerun()
        with nav_col2:
            if st.button("⚙️ Settings", use_container_width=True,
                         type="primary" if current_page == 'settings' else "secondary"):
                st.session_state.page = 'settings'
                st.rerun()


def create_hero_section():
    st.markdown("""
    <div class="hero-section">
        <h1 class="main-title">🚀 Cold Email Generator Pro</h1>
        <p class="subtitle">Transform job postings into powerful, personalized outreach emails that get responses</p>
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-number">95%</div>
                <div class="stat-label">Response Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">5s</div>
                <div class="stat-label">Generation Time</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">AI</div>
                <div class="stat-label">Powered</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_features_section():
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Precision Targeting</div>
            <div class="feature-description">Automatically extracts key requirements and tailors your message perfectly</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Lightning Fast</div>
            <div class="feature-description">Generate professional emails in seconds, not hours</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Portfolio Integration</div>
            <div class="feature-description">Seamlessly includes relevant work samples and achievements</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_loading_animation():
    placeholder = st.empty()
    placeholder.markdown("""
    <div class="loading-spinner">
        <div class="spinner"></div>
    </div>
    """, unsafe_allow_html=True)
    return placeholder


def home_page(llm, portfolio, clean_text):
    # Hero Section
    create_hero_section()

    # Main Input Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("### 🔗 Enter Job Posting URL")
        st.markdown("Paste the URL of any job posting to generate a tailored cold email")

        url_input = st.text_input(
            "Job URL:",
            value="https://jobs.nike.com/job/R-33460",
            label_visibility="collapsed",
            placeholder="https://example.com/job-posting",
            key="url_input"
        )

        submit_button = st.button("✨ Generate Cold Email", use_container_width=True, key="generate_btn")

    st.markdown('</div>', unsafe_allow_html=True)

    if submit_button:
        if url_input:
            # Show loading animation
            loading_placeholder = show_loading_animation()

            try:
                # Clear any previous results from session state
                if 'last_url' in st.session_state and st.session_state.last_url == url_input:
                    # Same URL, clear previous results to avoid duplication
                    if 'generated_emails' in st.session_state:
                        del st.session_state.generated_emails

                st.session_state.last_url = url_input

                # Load and process the URL
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)

                # Try to load portfolio but continue even if it fails
                portfolio_loaded = False
                try:
                    portfolio_loaded = portfolio.load_portfolio()
                except Exception as e:
                    st.info("ℹ️ No portfolio file found. Generating email without portfolio links.")

                jobs = llm.extract_jobs(data)

                # Clear loading animation
                loading_placeholder.empty()

                # Success message
                st.markdown("""
                <div class="success-message">
                    ✅ Email Generated Successfully! Your personalized cold email is ready.
                </div>
                """, unsafe_allow_html=True)

                # Store generated emails in session state to avoid regeneration
                if 'generated_emails' not in st.session_state:
                    st.session_state.generated_emails = {}

                for idx, job in enumerate(jobs):
                    job_key = f"{url_input}_{idx}"

                    # Job details section
                    with st.expander(f"📋 **Extracted Job Details - Position {idx + 1}**", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**🏢 Company:** {job.get('company', 'N/A')}")
                            st.markdown(f"**💼 Role:** {job.get('role', 'N/A')}")
                        with col2:
                            st.markdown(f"**📍 Location:** {job.get('location', 'N/A')}")
                            st.markdown(f"**🎯 Experience:** {job.get('experience', 'N/A')}")

                        if job.get('skills'):
                            st.markdown("**🛠️ Required Skills:**")
                            skills_cols = st.columns(4)
                            for skill_idx, skill in enumerate(job.get('skills', [])):
                                with skills_cols[skill_idx % 4]:
                                    st.markdown(f"• {skill}")

                    # Generate email only if not already generated for this job
                    if job_key not in st.session_state.generated_emails:
                        skills = job.get('skills', [])

                        # Query portfolio links
                        links = []
                        if portfolio_loaded:
                            try:
                                links = portfolio.query_links(skills)
                            except:
                                links = []

                        email = llm.write_mail(job, links)
                        st.session_state.generated_emails[job_key] = email
                    else:
                        email = st.session_state.generated_emails[job_key]

                    # Display generated email
                    st.markdown(f"### 📧 Your Personalized Cold Email - Position {idx + 1}")

                    # Create a unique key for this email's text area
                    email_key = f"email_text_{job_key}"
                    edited_email = st.text_area(
                        "Edit your email:",
                        value=email,
                        height=400,
                        key=email_key,
                        label_visibility="collapsed"
                    )

                    # Action buttons with unique keys
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"📋 Copy to Clipboard", use_container_width=True, key=f"copy_{idx}"):
                            # Using pyperclip alternative for Streamlit
                            st.code(edited_email, language='text')
                            st.success("Email displayed above - select and copy!")
                    with col2:
                        if st.button(f"🔄 Regenerate", use_container_width=True, key=f"regen_{idx}"):
                            # Clear this specific email from cache
                            if job_key in st.session_state.generated_emails:
                                del st.session_state.generated_emails[job_key]
                            st.rerun()
                    with col3:
                        if st.button(f"💾 Save Draft", use_container_width=True, key=f"save_{idx}"):
                            # Save to file
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"email_draft_{timestamp}.txt"
                            with open(filename, 'w') as f:
                                f.write(edited_email)
                            st.success(f"Draft saved as {filename}")

                    st.markdown("---")

            except Exception as e:
                loading_placeholder.empty()
                st.error(f"⚠️ An Error Occurred: {str(e)}")
                st.markdown("Please check the URL and try again.")
        else:
            st.warning("Please enter a valid job posting URL")

    # Features Section
    st.markdown("---")
    st.markdown("## 🌟 Why Choose Our Cold Email Generator?")
    create_features_section()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 2rem;">
        <p>Built with ❤️ using AI | Generate unlimited professional emails | 
        <a href="#" style="color: #667eea; text-decoration: none;">Learn More</a></p>
    </div>
    """, unsafe_allow_html=True)


def settings_page():
    st.markdown("## ⚙️ Professional Configuration")
    st.markdown("Configure your personal and professional details for personalized email generation")

    # Load existing config if available
    existing_config = st.session_state.get('user_config', {})

    with st.form("config_form"):
        # Personal Information Section
        st.markdown("""
        <div class="settings-card">
            <div class="settings-header">
                👤 Personal Information
                <span class="required-field">* Required fields</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            sender_name = st.text_input(
                "Your Name *",
                value=existing_config.get('sender_name', ''),
                placeholder="John Doe"
            )
            sender_email = st.text_input(
                "Email Address",
                value=existing_config.get('sender_email', ''),
                placeholder="john.doe@example.com"
            )
            sender_phone = st.text_input(
                "Phone Number",
                value=existing_config.get('sender_phone', ''),
                placeholder="+1 (555) 123-4567"
            )

        with col2:
            sender_title = st.text_input(
                "Your Title *",
                value=existing_config.get('sender_title', ''),
                placeholder="Business Development Manager"
            )
            years_experience = st.text_input(
                "Years of Experience",
                value=existing_config.get('years_experience', ''),
                placeholder="5+ years"
            )
            location = st.text_input(
                "Location",
                value=existing_config.get('location', ''),
                placeholder="San Francisco, CA"
            )

        # Social Links Section
        st.markdown("""
        <div class="settings-card" style="margin-top: 2rem;">
            <div class="settings-header">
                🔗 Professional Links
                <span class="optional-badge">Optional</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col3, col4 = st.columns(2)

        with col3:
            linkedin_url = st.text_input(
                "LinkedIn Profile",
                value=existing_config.get('linkedin_url', ''),
                placeholder="https://linkedin.com/in/johndoe"
            )
            portfolio_url = st.text_input(
                "Portfolio Website",
                value=existing_config.get('portfolio_url', ''),
                placeholder="https://johndoe.com"
            )

        with col4:
            github_url = st.text_input(
                "GitHub Profile",
                value=existing_config.get('github_url', ''),
                placeholder="https://github.com/johndoe"
            )
            twitter_url = st.text_input(
                "Twitter/X Profile",
                value=existing_config.get('twitter_url', ''),
                placeholder="https://twitter.com/johndoe"
            )

        # Company Information Section
        st.markdown("""
        <div class="settings-card" style="margin-top: 2rem;">
            <div class="settings-header">
                🏢 Company Information
                <span class="required-field">* At least company name required</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col5, col6 = st.columns(2)

        with col5:
            company_name = st.text_input(
                "Company Name *",
                value=existing_config.get('company_name', ''),
                placeholder="TechCorp Solutions"
            )
            company_type = st.text_input(
                "Industry/Type",
                value=existing_config.get('company_type', ''),
                placeholder="AI & Software Consulting"
            )
            company_website = st.text_input(
                "Company Website",
                value=existing_config.get('company_website', ''),
                placeholder="https://techcorp.com"
            )

        with col6:
            company_size = st.selectbox(
                "Company Size",
                ["", "1-10", "11-50", "51-200", "201-500", "500+"],
                index=["", "1-10", "11-50", "51-200", "201-500", "500+"].index(
                    existing_config.get('company_size', '')
                )
            )
            established_year = st.text_input(
                "Established Year",
                value=existing_config.get('established_year', ''),
                placeholder="2015"
            )

        # Email Preferences Section
        st.markdown("""
        <div class="settings-card" style="margin-top: 2rem;">
            <div class="settings-header">
                📧 Email Preferences
                <span class="optional-badge">Optional</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col7, col8 = st.columns(2)

        with col7:
            email_tone = st.selectbox(
                "Email Tone",
                ["professional", "casual", "formal", "friendly"],
                index=["professional", "casual", "formal", "friendly"].index(
                    existing_config.get('email_tone', 'professional')
                )
            )
            signature_style = st.selectbox(
                "Signature Style",
                ["standard", "detailed", "minimal", "with_social_links"],
                index=["standard", "detailed", "minimal", "with_social_links"].index(
                    existing_config.get('signature_style', 'standard')
                )
            )

        with col8:
            email_length = st.selectbox(
                "Preferred Email Length",
                ["short", "medium", "detailed"],
                index=["short", "medium", "detailed"].index(
                    existing_config.get('email_length', 'medium')
                )
            )
            include_portfolio = st.checkbox(
                "Auto-include portfolio links",
                value=existing_config.get('include_portfolio', True)
            )

        # Additional Information Section
        st.markdown("""
        <div class="settings-card" style="margin-top: 2rem;">
            <div class="settings-header">
                📝 Additional Information
                <span class="optional-badge">Optional</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        company_description = st.text_area(
            "Company Description",
            value=existing_config.get('company_description', ''),
            placeholder="Brief description of what your company does...",
            height=100
        )

        company_achievements = st.text_area(
            "Key Achievements & Clients",
            value=existing_config.get('company_achievements', ''),
            placeholder="Major clients, success metrics, awards, certifications...",
            height=100
        )

        unique_value_proposition = st.text_area(
            "Unique Value Proposition",
            value=existing_config.get('unique_value_proposition', ''),
            placeholder="What makes you/your company stand out...",
            height=100
        )

        save_button = st.form_submit_button("💾 Save Configuration", use_container_width=True)

        if save_button:
            # Only require name, title, and company name - everything else is optional
            if sender_name and sender_title and company_name:
                config = {
                    "sender_name": sender_name,
                    "sender_title": sender_title,
                    "sender_email": sender_email,
                    "sender_phone": sender_phone,
                    "years_experience": years_experience,
                    "location": location,
                    "linkedin_url": linkedin_url,
                    "github_url": github_url,
                    "portfolio_url": portfolio_url,
                    "twitter_url": twitter_url,
                    "company_name": company_name,
                    "company_type": company_type,
                    "company_website": company_website,
                    "company_size": company_size,
                    "established_year": established_year,
                    "company_description": company_description,
                    "company_achievements": company_achievements,
                    "unique_value_proposition": unique_value_proposition,
                    "email_tone": email_tone,
                    "signature_style": signature_style,
                    "email_length": email_length,
                    "include_portfolio": include_portfolio
                }

                # Save to session state
                st.session_state.user_config = config

                # Save to file
                with open("user_config.json", 'w') as f:
                    json.dump(config, f, indent=4)

                st.success("✅ Configuration saved successfully!")
                st.balloons()

                # Clear any cached chains to use new config
                if 'chain' in st.session_state:
                    del st.session_state.chain
            else:
                st.error("Please fill in the required fields: Name, Title, and Company Name")

    # Show current configuration preview
    if existing_config:
        st.markdown("---")
        with st.expander("📄 View Current Configuration", expanded=False):
            # Display configuration in a more organized way
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**👤 Personal Info**")
                st.markdown(f"Name: {existing_config.get('sender_name', 'N/A')}")
                st.markdown(f"Title: {existing_config.get('sender_title', 'N/A')}")
                st.markdown(f"Email: {existing_config.get('sender_email', 'N/A')}")

            with col2:
                st.markdown("**🏢 Company**")
                st.markdown(f"Name: {existing_config.get('company_name', 'N/A')}")
                st.markdown(f"Type: {existing_config.get('company_type', 'N/A')}")
                st.markdown(f"Size: {existing_config.get('company_size', 'N/A')}")

            with col3:
                st.markdown("**🔗 Social Links**")
                if existing_config.get('linkedin_url'):
                    st.markdown(f"[LinkedIn]({existing_config.get('linkedin_url')})")
                if existing_config.get('github_url'):
                    st.markdown(f"[GitHub]({existing_config.get('github_url')})")
                if existing_config.get('portfolio_url'):
                    st.markdown(f"[Portfolio]({existing_config.get('portfolio_url')})")

    # Quick actions
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

    with col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            if st.button("Confirm Reset?", key="confirm_reset"):
                st.session_state.user_config = {}
                if os.path.exists("user_config.json"):
                    os.remove("user_config.json")
                st.success("Configuration reset to defaults")
                st.rerun()

    with col3:
        if st.button("📥 Export Config", use_container_width=True):
            if existing_config:
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(existing_config, indent=4),
                    file_name="email_generator_config.json",
                    mime="application/json"
                )


def init_session_state():
    """Initialize session state with default values"""
    # Use query params to maintain state across refreshes
    query_params = st.query_params

    # Set page from query params or default to 'home'
    if 'page' not in st.session_state:
        page_from_url = query_params.get('page', 'home')
        st.session_state.page = page_from_url if page_from_url in ['home', 'settings'] else 'home'

    # Update query params to reflect current page
    st.query_params['page'] = st.session_state.page

    # Load saved configuration if exists
    if 'user_config' not in st.session_state:
        if os.path.exists("user_config.json"):
            with open("user_config.json", 'r') as f:
                st.session_state.user_config = json.load(f)
        else:
            st.session_state.user_config = None


if __name__ == "__main__":
    # Initialize session state
    init_session_state()

    # Inject custom CSS
    inject_custom_css()

    # Create navigation bar (appears on all pages)
    create_navigation_bar()

    # Sidebar for additional features
    with st.sidebar:
        st.markdown("### 🎯 Quick Navigation")

        # Navigation buttons in sidebar as backup
        if st.button("🏠 Home", use_container_width=True,
                     type="primary" if st.session_state.page == 'home' else "secondary",
                     key="sidebar_home"):
            st.session_state.page = 'home'
            st.query_params['page'] = 'home'
            st.rerun()

        if st.button("⚙️ Settings", use_container_width=True,
                     type="primary" if st.session_state.page == 'settings' else "secondary",
                     key="sidebar_settings"):
            st.session_state.page = 'settings'
            st.query_params['page'] = 'settings'
            st.rerun()

        st.markdown("---")

        # Portfolio upload section
        st.markdown("### 📁 Portfolio Management")
        uploaded_file = st.file_uploader("Upload Portfolio CSV", type=['csv'])
        if uploaded_file is not None:
            # Create directory if it doesn't exist
            os.makedirs("app/resource", exist_ok=True)
            # Save the uploaded file
            with open("app/resource/my_portfolio.csv", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("Portfolio uploaded successfully!")

        # Show current user if configured
        if st.session_state.user_config:
            st.markdown("---")
            st.markdown("### 👤 Current User")
            st.markdown(f"**{st.session_state.user_config['sender_name']}**")
            st.markdown(f"*{st.session_state.user_config['sender_title']}*")
            st.markdown(f"🏢 {st.session_state.user_config['company_name']}")

            # Show social links if available
            social_links = []
            if st.session_state.user_config.get('linkedin_url'):
                social_links.append("[LinkedIn](" + st.session_state.user_config['linkedin_url'] + ")")
            if st.session_state.user_config.get('github_url'):
                social_links.append("[GitHub](" + st.session_state.user_config['github_url'] + ")")

            if social_links:
                st.markdown("🔗 " + " | ".join(social_links))

        # Quick stats
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Emails Generated",
                      len(st.session_state.get('generated_emails', {})))
        with col2:
            st.metric("Portfolio Items",
                      "Active" if os.path.exists("app/resource/my_portfolio.csv") else "None")

    # Main content area - Display appropriate page based on state
    if st.session_state.page == 'settings':
        settings_page()
    else:  # home page
        # Check if configuration exists
        if not st.session_state.user_config:
            st.info("ℹ️ Welcome! Please configure your details before generating emails.")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("⚙️ Go to Settings", use_container_width=True, type="primary"):
                    st.session_state.page = 'settings'
                    st.query_params['page'] = 'settings'
                    st.rerun()
        else:
            # Create chain with user config, cache it in session state
            if 'chain' not in st.session_state:
                st.session_state.chain = Chain(st.session_state.user_config)

            chain = st.session_state.chain
            portfolio = Portfolio()
            home_page(chain, portfolio, clean_text)
import streamlit as st
from pathlib import Path

from app.builder.builder_ui import show_resume_builder


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Resume Scanner",
    page_icon="🤖",
    layout="wide"
)


# =====================================================
# LOAD CUSTOM CSS
# =====================================================

css_path = Path("assets/style.css")

with open(css_path, "r", encoding="utf-8") as file:
    st.markdown(
        f"<style>{file.read()}</style>",
        unsafe_allow_html=True
    )


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

st.sidebar.title("🤖 AI Resume Scanner")

st.sidebar.caption("AI-Powered Career Assistant")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📄 Resume Scanner",
        "🎯 Career Assistant",
        "✍️ Resume Builder",
        "📋 Application Tracker"
    ]
)


# =====================================================
# DASHBOARD
# =====================================================

if page == "🏠 Dashboard":

    st.title("🤖 AI Resume Scanner")

    st.write("Your AI-powered career workspace")

    st.markdown("---")

    st.subheader("Welcome back 👋")

    st.write(
        "Analyze your resume, discover suitable career paths, "
        "find matching jobs, and build a professional resume."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- STATISTICS ----------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="📄 Resume Score",
            value="82%"
        )

    with col2:
        st.metric(
            label="🎯 Career Readiness",
            value="76%"
        )

    with col3:
        st.metric(
            label="💼 Job Matches",
            value="24"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- QUICK ACTIONS ----------

    st.subheader("Quick Actions")

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "📄 Analyze Resume",
            use_container_width=True
        )

    with col2:
        st.button(
            "✍️ Build Resume",
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- RECENT ACTIVITY ----------

    st.subheader("Recent Activity")

    st.info("📄 Resume analysis — Ready to use")

    st.info("🎯 Career prediction — Ready to use")

    st.info("💼 Job matching — Ready to use")


# =====================================================
# RESUME SCANNER
# =====================================================

elif page == "📄 Resume Scanner":

    st.title("📄 Resume Scanner")

    st.write(
        "Upload your resume to analyze skills, education, "
        "experience and overall resume quality."
    )

    st.info(
        "Resume Scanner backend will be connected here."
    )


# =====================================================
# CAREER ASSISTANT
# =====================================================

elif page == "🎯 Career Assistant":

    st.title("🎯 Career Assistant")

    st.write(
        "Discover suitable career paths, readiness scores "
        "and personalized career roadmaps."
    )

    st.info(
        "Career Engine will be connected here."
    )


# =====================================================
# RESUME BUILDER
# =====================================================

elif page == "✍️ Resume Builder":

    show_resume_builder()


# =====================================================
# APPLICATION TRACKER
# =====================================================

elif page == "📋 Application Tracker":

    st.title("📋 Application Tracker")

    st.write(
        "Track your job and internship applications "
        "from one place."
    )

    st.info(
        "Application Tracker will be connected here."
    )
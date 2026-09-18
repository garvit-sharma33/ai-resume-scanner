from datetime import date
from pathlib import Path
import html

import streamlit as st

from app.resume.parser import extract_resume_text
from app.resume.analyzer import analyze_resume

from app.jobs.jobs import (
    fetch_jobs,
    clean_job_data,
    rank_jobs,
)

from app.career.career import (
    generate_career_roadmap,
    calculate_job_readiness,
    get_career_recommendation,
)

from app.ai.gemini import generate_career_advice

from app.builder.builder_ui import show_resume_builder

from app.tracker.tracker import (
    create_table,
    add_application,
    get_applications,
    update_application_status,
    delete_application,
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Scanner",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DATABASE
# =========================================================

create_table()


# =========================================================
# LOAD CSS
# =========================================================

CSS_FILE = Path("assets/style.css")

if CSS_FILE.exists():

    css = CSS_FILE.read_text(
        encoding="utf-8"
    )

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def safe(value):
    """
    Safely convert values to HTML text.
    """

    return html.escape(
        str(value or "")
    )


def html_card(
    content,
    class_name="custom-card"
):
    """
    Render trusted HTML inside a styled card.
    """

    st.markdown(
        f"""
        <div class="{class_name}">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )


def page_header(
    kicker,
    title,
    subtitle
):
    """
    Common page header.
    """

    st.markdown(
        f"""
        <div class="page-kicker">
            {safe(kicker)}
        </div>

        <h1 class="page-title">
            {safe(title)}
        </h1>

        <p class="page-subtitle">
            {safe(subtitle)}
        </p>
        """,
        unsafe_allow_html=True
    )


def metric_card(
    icon,
    label,
    value,
    note=""
):
    """
    Reusable dashboard metric card.
    """

    html_card(
        f"""
        <div class="metric-icon">
            {icon}
        </div>

        <div class="metric-label">
            {safe(label)}
        </div>

        <div class="metric-value">
            {safe(value)}
        </div>

        <div class="metric-note">
            {safe(note)}
        </div>
        """,
        "metric-card"
    )


def skill_chips(skills):
    """
    Display detected skills as chips.
    """

    if not skills:

        st.markdown(
            """
            <div class="muted-text">
                No skills detected.
            </div>
            """,
            unsafe_allow_html=True
        )

        return

    chips = ""

    for skill in skills:

        chips += f"""
        <span class="skill-chip">
            {safe(skill)}
        </span>
        """

    st.markdown(
        f"""
        <div class="skills-container">
            {chips}
        </div>
        """,
        unsafe_allow_html=True
    )


def score_ring(score):
    """
    Display resume score as circular progress.
    """

    try:
        score = int(score or 0)

    except Exception:
        score = 0

    score = max(
        0,
        min(100, score)
    )

    st.markdown(
        f"""
        <div class="score-wrap">

            <div
                class="score-ring"
                style="
                    background:
                    conic-gradient(
                        #3B82F6 {score}%,
                        #1E293B {score}%
                    );
                "
            >

                <div class="score-inner">

                    <div class="score-number">
                        {score}%
                    </div>

                    <div class="score-label">
                        Resume Score
                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def status_badge(status):
    """
    Create application status badge.
    """

    status = str(
        status or "Unknown"
    )

    status_class = {
        "Applied": "status-applied",
        "Interview": "status-interview",
        "Selected": "status-selected",
        "Rejected": "status-rejected",
        "Withdrawn": "status-withdrawn",
    }.get(
        status,
        "status-applied"
    )

    return f"""
    <span class="status-badge {status_class}">
        {safe(status)}
    </span>
    """


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">

            <div class="brand-icon">
                🤖
            </div>

            <div>

                <div class="brand-title">
                    ResumeAI
                </div>

                <div class="brand-subtitle">
                    Career Intelligence
                </div>

            </div>

        </div>

        <div class="sidebar-label">
            WORKSPACE
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",

        [
            "🏠 Dashboard",
            "📄 Resume Scanner",
            "🎯 Career Assistant",
            "💼 Job Matches",
            "✍️ Resume Builder",
            "📋 Application Tracker",
        ],

        label_visibility="collapsed"
    )

    st.markdown(
        """
        <div class="sidebar-footer">

            <div>
                AI Resume Scanner
            </div>

            <small>
                Build skills. Find roles. Get hired.
            </small>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    page_header(
        "AI CAREER INTELLIGENCE",
        "Career Dashboard",
        "Your resume, skills and opportunities — in one workspace."
    )

    result = st.session_state.get(
        "resume_data"
    )

    # -----------------------------------------------------
    # EMPTY DASHBOARD
    # -----------------------------------------------------

    if not result:

        html_card(
            """
            <div class="hero-icon">
                📄
            </div>

            <div class="hero-kicker">
                GET STARTED
            </div>

            <h2>
                Start with your resume
            </h2>

            <p>
                Upload your resume to unlock resume analysis,
                career recommendations, skill-gap detection
                and job matching.
            </p>
            """,
            "hero-card"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            metric_card(
                "📊",
                "Resume Intelligence",
                "Ready",
                "Skills & quality analysis"
            )

        with col2:

            metric_card(
                "🎯",
                "Career Intelligence",
                "Ready",
                "Career paths & roadmap"
            )

        with col3:

            metric_card(
                "💼",
                "Job Intelligence",
                "Ready",
                "Live job matching"
            )

        st.info(
            "Go to **Resume Scanner** "
            "from the sidebar to begin."
        )

    # -----------------------------------------------------
    # DASHBOARD WITH RESUME DATA
    # -----------------------------------------------------

    else:

        score = result.get(
            "resume_score",
            0
        )

        skills = result.get(
            "skills",
            []
        )

        careers = result.get(
            "job_matches",
            []
        )

        applications = get_applications()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            metric_card(
                "📄",
                "Resume Score",
                f"{score}%",
                "Overall resume quality"
            )

        with col2:

            metric_card(
                "🛠️",
                "Skills",
                str(len(skills)),
                "Detected skills"
            )

        with col3:

            metric_card(
                "🎯",
                "Career Matches",
                str(len(careers)),
                "Potential career paths"
            )

        with col4:

            metric_card(
                "📋",
                "Applications",
                str(len(applications)),
                "Tracked applications"
            )

        st.markdown(
            "<div class='section-gap'></div>",
            unsafe_allow_html=True
        )

        left, right = st.columns(
            [1, 2]
        )

        with left:

            html_card(
                """
                <h3>
                    Resume Health
                </h3>

                <p>
                    Your current resume score.
                </p>
                """,
                "section-card"
            )

            score_ring(score)

        with right:

            html_card(
                """
                <h3>
                    Detected Skills
                </h3>

                <p>
                    Skills extracted from your resume.
                </p>
                """,
                "section-card"
            )

            skill_chips(skills)

            if careers:

                st.markdown(
                    "### 🎯 Career Matches"
                )

                for career in careers[:5]:

                    career_name = career.get(
                        "career",
                        "Unknown"
                    )

                    match_percentage = int(
                        career.get(
                            "match_percentage",
                            0
                        )
                    )

                    st.progress(
                        min(
                            100,
                            match_percentage
                        ) / 100
                    )

                    st.caption(
                        f"{career_name} — "
                        f"{match_percentage}% match"
                    )


    # =========================================================
# RESUME SCANNER
# =========================================================

elif page == "📄 Resume Scanner":

    page_header(
        "RESUME INTELLIGENCE",
        "Resume Scanner",
        "Upload a PDF or DOCX and turn your resume into actionable career insights."
    )

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        help="Supported formats: PDF and DOCX"
    )

    if uploaded_file:

        extension = Path(
            uploaded_file.name
        ).suffix.lower()

        temp_path = Path(
            "temp_resume" + extension
        )

        temp_path.write_bytes(
            uploaded_file.getbuffer()
        )

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        if st.button(
            "🧠 Analyze Resume",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Extracting and analyzing your resume..."
                ):

                    resume_text = extract_resume_text(
                        str(temp_path)
                    )

                    if not resume_text or not resume_text.strip():

                        st.error(
                            "No readable text was found in this resume. "
                            "Try a text-based PDF or DOCX file."
                        )

                    else:

                        resume_result = analyze_resume(
                            resume_text
                        )

                        st.session_state[
                            "resume_data"
                        ] = resume_result

                        st.session_state[
                            "resume_text"
                        ] = resume_text

                        st.success(
                            "Resume analyzed successfully!"
                        )

                        st.rerun()

            except Exception as error:

                st.error(
                    f"Resume analysis failed: {error}"
                )

    # -----------------------------------------------------
    # ANALYSIS RESULT
    # -----------------------------------------------------

    result = st.session_state.get(
        "resume_data"
    )

    if result:

        st.markdown(
            "<div class='section-gap'></div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "## 📊 Analysis Results"
        )

        # -------------------------------------------------
        # TOP METRICS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(
            [1, 1, 2]
        )

        with col1:

            score_ring(
                result.get(
                    "resume_score",
                    0
                )
            )

        with col2:

            metric_card(
                "🛠️",
                "Total Skills",
                str(
                    result.get(
                        "total_skills",
                        len(
                            result.get(
                                "skills",
                                []
                            )
                        )
                    )
                ),
                "Detected in resume"
            )

            metric_card(
                "⭐",
                "Resume Rating",
                result.get(
                    "resume_rating",
                    "N/A"
                ),
                "Resume quality"
            )

        with col3:

            html_card(
                f"""
                <h3>
                    👤 Candidate Profile
                </h3>

                <p>
                    <strong>Name:</strong>
                    {safe(
                        result.get(
                            "name",
                            "Not detected"
                        )
                    )}
                </p>

                <p>
                    <strong>Email:</strong>
                    {safe(
                        result.get(
                            "email",
                            "Not detected"
                        )
                    )}
                </p>

                <p>
                    <strong>Phone:</strong>
                    {safe(
                        result.get(
                            "phone",
                            "Not detected"
                        )
                    )}
                </p>
                """,
                "section-card"
            )

        # -------------------------------------------------
        # SKILLS
        # -------------------------------------------------

        st.markdown(
            "### 🛠️ Detected Skills"
        )

        skill_chips(
            result.get(
                "skills",
                []
            )
        )

        # -------------------------------------------------
        # EDUCATION + EXPERIENCE
        # -------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            html_card(
                """
                <h3>
                    🎓 Education
                </h3>
                """,
                "section-card"
            )

            education = result.get(
                "education",
                []
            )

            if education:

                for item in education:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.caption(
                    "No education details detected."
                )

        with col2:

            html_card(
                """
                <h3>
                    💼 Experience
                </h3>
                """,
                "section-card"
            )

            experience = result.get(
                "experience",
                []
            )

            if experience:

                for item in experience:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.caption(
                    "No experience details detected."
                )

        # -------------------------------------------------
        # CAREER MATCHES
        # -------------------------------------------------

        st.markdown(
            "### 🎯 Career Matches"
        )

        career_matches = result.get(
            "job_matches",
            []
        )

        if career_matches:

            for career in career_matches[:5]:

                career_name = career.get(
                    "career",
                    "Unknown"
                )

                match_percentage = int(
                    career.get(
                        "match_percentage",
                        0
                    )
                )

                st.progress(
                    min(
                        100,
                        match_percentage
                    ) / 100
                )

                st.write(
                    f"**{career_name}** — "
                    f"{match_percentage}% match"
                )

        else:

            st.info(
                "No career matches available."
            )

        # -------------------------------------------------
        # SKILL GAPS + SUGGESTIONS
        # -------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            html_card(
                """
                <h3>
                    📚 Skill Gaps
                </h3>
                """,
                "section-card"
            )

            skill_gaps = result.get(
                "skill_gaps",
                []
            )

            if skill_gaps:

                for gap in skill_gaps:

                    st.write(
                        f"• {gap}"
                    )

            else:

                st.success(
                    "No major skill gaps detected."
                )

        with col2:

            html_card(
                """
                <h3>
                    💡 Skill Suggestions
                </h3>
                """,
                "section-card"
            )

            suggestions = result.get(
                "skill_suggestions",
                []
            )

            if suggestions:

                for item in suggestions[:8]:

                    if isinstance(
                        item,
                        dict
                    ):

                        skill = item.get(
                            "skill",
                            "Skill"
                        )

                        suggestion = item.get(
                            "suggestion",
                            ""
                        )

                        st.write(
                            f"**{skill}:** {suggestion}"
                        )

                    else:

                        st.write(
                            f"• {item}"
                        )

            else:

                st.caption(
                    "No suggestions available."
                )

        # -------------------------------------------------
        # EXTRACTED TEXT
        # -------------------------------------------------

        with st.expander(
            "🔍 View Extracted Resume Text"
        ):

            st.text(
                st.session_state.get(
                    "resume_text",
                    ""
                )
            )


# =========================================================
# CAREER ASSISTANT
# =========================================================

elif page == "🎯 Career Assistant":

    page_header(
        "CAREER INTELLIGENCE",
        "AI Career Assistant",
        "Understand your career direction, readiness and next learning steps."
    )

    result = st.session_state.get(
        "resume_data"
    )

    if not result:

        st.info(
            "Analyze a resume first from "
            "**Resume Scanner**."
        )

    else:

        skills = result.get(
            "skills",
            []
        )

        career_matches = result.get(
            "job_matches",
            []
        )

        if not career_matches:

            st.warning(
                "No career path was detected "
                "from the current resume."
            )

        else:

            try:

                best_career = career_matches[0].get(
                    "career",
                    "Unknown"
                )

                roadmap = generate_career_roadmap(
                    best_career,
                    skills
                )

                career_readiness = roadmap.get(
                    "readiness",
                    0
                )

                job_readiness = calculate_job_readiness(
                    result.get(
                        "resume_score",
                        0
                    ),
                    career_readiness
                )

                recommendation = get_career_recommendation(
                    career_readiness
                )

                # -----------------------------------------
                # CAREER METRICS
                # -----------------------------------------

                col1, col2, col3 = st.columns(3)

                with col1:

                    metric_card(
                        "🎯",
                        "Recommended Career",
                        best_career,
                        "Current career match"
                    )

                with col2:

                    metric_card(
                        "📈",
                        "Career Readiness",
                        f"{career_readiness}%",
                        "Roadmap readiness"
                    )

                with col3:

                    metric_card(
                        "💼",
                        "Job Readiness",
                        f"{job_readiness}%",
                        "Combined readiness"
                    )

                # -----------------------------------------
                # RECOMMENDATION
                # -----------------------------------------

                html_card(
                    f"""
                    <h3>
                        ⭐ Career Recommendation
                    </h3>

                    <p>
                        {safe(recommendation)}
                    </p>
                    """,
                    "highlight-card"
                )

                # -----------------------------------------
                # CAREER PREDICTIONS
                # -----------------------------------------

                st.markdown(
                    "### 🚀 Career Predictions"
                )

                for career in career_matches[:5]:

                    career_name = career.get(
                        "career",
                        "Unknown"
                    )

                    percentage = int(
                        career.get(
                            "match_percentage",
                            0
                        )
                    )

                    st.progress(
                        min(
                            100,
                            percentage
                        ) / 100
                    )

                    st.write(
                        f"**{career_name}** — "
                        f"{percentage}% match"
                    )

                # -----------------------------------------
                # MISSING SKILLS + ROADMAP
                # -----------------------------------------

                missing_skills = roadmap.get(
                    "missing_skills",
                    []
                )

                roadmap_steps = roadmap.get(
                    "roadmap_steps",
                    []
                )

                col1, col2 = st.columns(2)

                with col1:

                    html_card(
                        """
                        <h3>
                            📚 Skills to Learn
                        </h3>
                        """,
                        "section-card"
                    )

                    if missing_skills:

                        for skill in missing_skills:

                            st.write(
                                f"• {skill}"
                            )

                    else:

                        st.success(
                            "You already cover the "
                            "required skills."
                        )

                with col2:

                    html_card(
                        """
                        <h3>
                            🗺️ Career Roadmap
                        </h3>
                        """,
                        "section-card"
                    )

                    if roadmap_steps:

                        for index, step in enumerate(
                            roadmap_steps,
                            1
                        ):

                            st.write(
                                f"**Step {index}:** {step}"
                            )

                    else:

                        st.caption(
                            "No roadmap steps available."
                        )

                # -----------------------------------------
                # GEMINI AI ADVICE
                # -----------------------------------------

                st.markdown(
                    "### 🤖 Gemini Career Advice"
                )

                if st.button(
                    "🧠 Generate Personalized AI Advice",
                    type="primary",
                    use_container_width=True
                ):

                    try:

                        with st.spinner(
                            "Gemini is preparing your personalized advice..."
                        ):

                            advice = generate_career_advice(
                                skills=", ".join(skills),
                                career=best_career,
                                missing_skills=", ".join(
                                    missing_skills
                                )
                            )

                        html_card(
                            f"""
                            <h3>
                                💡 Personalized Advice
                            </h3>

                            <div class="ai-response">
                                {safe(advice)}
                            </div>
                            """,
                            "ai-card"
                        )

                    except Exception as error:

                        st.error(
                            f"AI advice failed: {error}"
                        )

            except Exception as error:

                st.error(
                    f"Career analysis failed: {error}"
                )

    # =========================================================
# JOB MATCHES
# =========================================================

elif page == "💼 Job Matches":

    page_header(
        "JOB INTELLIGENCE",
        "Recommended Jobs",
        "Live opportunities ranked according to the skills detected in your resume."
    )

    result = st.session_state.get(
        "resume_data"
    )

    if not result:

        st.info(
            "Analyze a resume first from "
            "**Resume Scanner**."
        )

    else:

        if st.button(
            "🔎 Find Matching Jobs",
            type="primary",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Finding matching jobs..."
                ):

                    live_jobs = fetch_jobs(
                        limit=20
                    )

                    cleaned_jobs = clean_job_data(
                        live_jobs
                    )

                    ranked_jobs = rank_jobs(
                        result.get(
                            "skills",
                            []
                        ),
                        cleaned_jobs
                    )

                    st.session_state[
                        "ranked_jobs"
                    ] = ranked_jobs

            except Exception as error:

                st.error(
                    f"Job search failed: {error}"
                )

        jobs = st.session_state.get(
            "ranked_jobs",
            []
        )

        if not jobs:

            st.info(
                "Click **Find Matching Jobs** "
                "to load current opportunities."
            )

        else:

            st.success(
                f"Found {len(jobs)} matching jobs."
            )

            for index, job in enumerate(
                jobs[:10],
                1
            ):

                title = safe(
                    job.get(
                        "title",
                        "Untitled role"
                    )
                )

                company = safe(
                    job.get(
                        "company",
                        "Unknown company"
                    )
                )

                location = safe(
                    job.get(
                        "location",
                        "Not specified"
                    )
                )

                job_type = safe(
                    job.get(
                        "type",
                        "Not specified"
                    )
                )

                match_percentage = int(
                    job.get(
                        "match_percentage",
                        0
                    )
                )

                match_label = safe(
                    job.get(
                        "match_label",
                        "Match"
                    )
                )

                # -----------------------------------------
                # JOB CARD
                # -----------------------------------------

                html_card(
                    f"""
                    <div class="job-top">

                        <div>

                            <div class="job-number">
                                JOB {index}
                            </div>

                            <h2>
                                {title}
                            </h2>

                            <p>
                                🏢 {company}
                            </p>

                            <p>
                                📍 {location}
                                &nbsp; • &nbsp;
                                💼 {job_type}
                            </p>

                        </div>

                        <div class="job-match">

                            <strong>
                                {match_percentage}%
                            </strong>

                            <span>
                                {match_label}
                            </span>

                        </div>

                    </div>
                    """,
                    "job-card"
                )

                # -----------------------------------------
                # MATCHED SKILLS
                # -----------------------------------------

                matched_skills = job.get(
                    "matched_skills",
                    []
                )

                if matched_skills:

                    st.markdown(
                        "**✅ Matched Skills**"
                    )

                    skill_chips(
                        matched_skills
                    )

                # -----------------------------------------
                # MISSING SKILLS
                # -----------------------------------------

                missing_required = job.get(
                    "missing_required",
                    []
                )

                missing_preferred = job.get(
                    "missing_preferred",
                    []
                )

                missing_skills = (
                    missing_required
                    + missing_preferred
                )

                if missing_skills:

                    st.markdown(
                        "**📚 Missing Skills**"
                    )

                    skill_chips(
                        missing_skills
                    )

                # -----------------------------------------
                # JOB ACTIONS
                # -----------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    apply_link = job.get(
                        "apply_link"
                    )

                    if apply_link:

                        st.link_button(
                            "🚀 Apply Now",
                            apply_link,
                            use_container_width=True
                        )

                with col2:

                    if st.button(
                        "📋 Track Job",
                        key=f"track_job_{index}",
                        use_container_width=True
                    ):

                        add_application(
                            company=job.get(
                                "company",
                                ""
                            ),
                            role=job.get(
                                "title",
                                ""
                            ),
                            location=job.get(
                                "location",
                                ""
                            ),
                            status="Applied",
                            applied_date=str(
                                date.today()
                            ),
                            job_url=job.get(
                                "apply_link",
                                ""
                            )
                        )

                        st.success(
                            "Job added to Application Tracker."
                        )

                st.markdown(
                    "<div class='card-gap'></div>",
                    unsafe_allow_html=True
                )


# =========================================================
# RESUME BUILDER
# =========================================================

elif page == "✍️ Resume Builder":

    page_header(
        "DOCUMENT STUDIO",
        "Resume Builder",
        "Create a clean professional resume from your information."
    )

    show_resume_builder()


# =========================================================
# APPLICATION TRACKER
# =========================================================

elif page == "📋 Application Tracker":

    page_header(
        "APPLICATION MANAGEMENT",
        "Application Tracker",
        "Track your applications, interviews and outcomes in one place."
    )

    all_applications = get_applications()

    # -----------------------------------------------------
    # TRACKER METRICS
    # -----------------------------------------------------

    total_applications = len(
        all_applications
    )

    applied_count = sum(
        1
        for application in all_applications
        if application[4] == "Applied"
    )

    interview_count = sum(
        1
        for application in all_applications
        if application[4] == "Interview"
    )

    selected_count = sum(
        1
        for application in all_applications
        if application[4] == "Selected"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        metric_card(
            "📋",
            "Total",
            str(total_applications),
            "All applications"
        )

    with col2:

        metric_card(
            "📨",
            "Applied",
            str(applied_count),
            "Active applications"
        )

    with col3:

        metric_card(
            "🎤",
            "Interviews",
            str(interview_count),
            "Interview stage"
        )

    with col4:

        metric_card(
            "🎉",
            "Selected",
            str(selected_count),
            "Successful outcomes"
        )

    st.markdown(
        "<div class='section-gap'></div>",
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # ADD APPLICATION
    # -----------------------------------------------------

    with st.expander(
        "➕ Add New Application"
    ):

        col1, col2 = st.columns(2)

        with col1:

            company = st.text_input(
                "Company"
            )

            role = st.text_input(
                "Job Role"
            )

            location = st.text_input(
                "Location"
            )

        with col2:

            status = st.selectbox(
                "Status",
                [
                    "Applied",
                    "Interview",
                    "Selected",
                    "Rejected",
                    "Withdrawn"
                ]
            )

            applied_date = st.date_input(
                "Applied Date",
                value=date.today()
            )

            job_url = st.text_input(
                "Job URL"
            )

        if st.button(
            "➕ Add Application",
            type="primary",
            use_container_width=True
        ):

            if (
                not company.strip()
                or not role.strip()
            ):

                st.warning(
                    "Company and Job Role are required."
                )

            else:

                add_application(
                    company=company.strip(),
                    role=role.strip(),
                    location=location.strip(),
                    status=status,
                    applied_date=str(
                        applied_date
                    ),
                    job_url=job_url.strip()
                )

                st.success(
                    "Application added successfully."
                )

                st.rerun()

    # -----------------------------------------------------
    # FILTER
    # -----------------------------------------------------

    st.markdown(
        "### 📋 Your Applications"
    )

    filter_status = st.selectbox(
        "Filter Applications",
        [
            "All",
            "Applied",
            "Interview",
            "Selected",
            "Rejected",
            "Withdrawn"
        ]
    )

    if filter_status == "All":

        filtered_applications = (
            all_applications
        )

    else:

        filtered_applications = [
            application
            for application in all_applications
            if application[4] == filter_status
        ]

    # -----------------------------------------------------
    # APPLICATION LIST
    # -----------------------------------------------------

    if not filtered_applications:

        st.info(
            "No applications found."
        )

    else:

        for application in filtered_applications:

            (
                application_id,
                company_name,
                job_role,
                job_location,
                current_status,
                applied_on,
                application_url
            ) = application

            # ---------------------------------------------
            # APPLICATION CARD
            # ---------------------------------------------

            html_card(
                f"""
                <div class="application-number">
                    APPLICATION #{application_id}
                </div>

                <h2>
                    {safe(job_role)}
                </h2>

                <p>
                    🏢 {safe(company_name)}
                </p>

                <p>
                    📍 {safe(
                        job_location
                        or "Location not provided"
                    )}
                </p>

                <p>
                    📅 Applied:
                    {safe(
                        applied_on
                        or "N/A"
                    )}
                </p>

                <div>
                    {status_badge(
                        current_status
                    )}
                </div>
                """,
                "application-card"
            )

            status_options = [
                "Applied",
                "Interview",
                "Selected",
                "Rejected",
                "Withdrawn"
            ]

            col1, col2, col3 = st.columns(
                [2, 2, 1]
            )

            # ---------------------------------------------
            # UPDATE STATUS
            # ---------------------------------------------

            with col1:

                current_index = (
                    status_options.index(
                        current_status
                    )
                    if current_status
                    in status_options
                    else 0
                )

                new_status = st.selectbox(
                    "Update Status",
                    status_options,
                    index=current_index,
                    key=f"status_{application_id}"
                )

            with col2:

                if st.button(
                    "🔄 Update Status",
                    key=f"update_{application_id}",
                    use_container_width=True
                ):

                    update_application_status(
                        application_id,
                        new_status
                    )

                    st.success(
                        "Status updated successfully."
                    )

                    st.rerun()

            # ---------------------------------------------
            # DELETE
            # ---------------------------------------------

            with col3:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{application_id}",
                    use_container_width=True
                ):

                    delete_application(
                        application_id
                    )

                    st.success(
                        "Application deleted."
                    )

                    st.rerun()

            # ---------------------------------------------
            # JOB LINK
            # ---------------------------------------------

            if application_url:

                st.link_button(
                    "🔗 Open Job Link",
                    application_url,
                    use_container_width=True
                )

            st.markdown(
                "<div class='card-gap'></div>",
                unsafe_allow_html=True
            )
import streamlit as st
from pathlib import Path

from app.builder.builder_ui import show_resume_builder

from app.tracker.tracker import (
    create_table,
    add_application,
    get_applications,
    update_application_status,
    delete_application
)


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Resume Scanner",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# INITIALIZE DATABASE
# =====================================================

# Create the application table when the app starts
create_table()

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

    st.markdown("---")

    # =================================================
    # ADD NEW APPLICATION
    # =================================================

    st.subheader("➕ Add New Application")

    col1, col2 = st.columns(2)

    with col1:
        company = st.text_input("Company Name")
        role = st.text_input("Job Role")
        location = st.text_input("Location")

    with col2:
        status = st.selectbox(
            "Application Status",
            [
                "Applied",
                "Interview",
                "Selected",
                "Rejected",
                "Withdrawn"
            ]
        )

        applied_date = st.date_input(
            "Applied Date"
        )

        job_url = st.text_input("Job URL")

    if st.button(
        "➕ Add Application",
        type="primary",
        use_container_width=True
    ):

        if not company.strip() or not role.strip():

            st.warning(
                "Please enter company name and job role."
            )

        else:

            add_application(
                company=company.strip(),
                role=role.strip(),
                location=location.strip(),
                status=status,
                applied_date=str(applied_date),
                job_url=job_url.strip()
            )

            st.success(
                "Application added successfully!"
            )

            st.rerun()


    # =================================================
    # APPLICATION LIST
    # =================================================

    st.markdown("---")

    st.subheader("📋 Your Applications")

    # =================================================
    # APPLICATION STATISTICS
    # =================================================

    all_applications = get_applications()

    total = len(all_applications)

    applied_count = sum(
        1 for app in all_applications
        if app[4] == "Applied"
    )

    interview_count = sum(
        1 for app in all_applications
        if app[4] == "Interview"
    )

    selected_count = sum(
        1 for app in all_applications
        if app[4] == "Selected"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📋 Total", total)

    with col2:
        st.metric("📨 Applied", applied_count)

    with col3:
        st.metric("🎤 Interviews", interview_count)

    with col4:
        st.metric("🎉 Selected", selected_count)


    # =================================================
    # STATUS FILTER
    # =================================================

    filter_status = st.selectbox(
        "🔎 Filter Applications",
        [
            "All",
            "Applied",
            "Interview",
            "Selected",
            "Rejected",
            "Withdrawn"
        ]
    )


    # =================================================
    # FILTER APPLICATIONS
    # =================================================

    if filter_status == "All":

        applications = all_applications

    else:

        applications = [
            app
            for app in all_applications
            if app[4] == filter_status
        ]

    if not applications:

        st.info(
            "No applications added yet."
        )

    else:

        for application in applications:

            application_id = application[0]
            company_name = application[1]
            job_role = application[2]
            job_location = application[3]
            application_status = application[4]
            date_applied = application[5]
            application_url = application[6]

            with st.container():

                st.markdown(
                    f"### 💼 {job_role}"
                )

                st.write(
                    f"**Company:** {company_name}"
                )

                st.write(
                    f"**Location:** {job_location or 'Not specified'}"
                )

                st.write(
                    f"**Applied:** {date_applied}"
                )

                st.write(
                    f"**Status:** {application_status}"
                )

                if application_url:
                    st.write(
                        f"🔗 {application_url}"
                    )


                # =================================================
                # UPDATE STATUS
                # =================================================

                new_status = st.selectbox(
                    "Update Status",
                    [
                        "Applied",
                        "Interview",
                        "Selected",
                        "Rejected",
                        "Withdrawn"
                    ],
                    index=[
                        "Applied",
                        "Interview",
                        "Selected",
                        "Rejected",
                        "Withdrawn"
                    ].index(application_status),
                    key=f"status_{application_id}"
                )


                col1, col2 = st.columns(2)

                with col1:
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
                            "Application status updated!"
                        )

                        st.rerun()


                with col2:
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{application_id}",
                        use_container_width=True
                    ):
                        delete_application(
                            application_id
                        )

                        st.success(
                            "Application deleted!"
                        )

                        st.rerun()


                st.markdown("---")
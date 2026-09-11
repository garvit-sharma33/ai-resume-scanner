import streamlit as st

from app.builder.resume_builder import (
    create_resume_data,
    generate_resume_text
)


def show_resume_builder():
    """
    Displays the Resume Builder interface.
    Users can enter personal information, skills,
    education, experience and multiple projects.
    """

    st.title("✍️ Resume Builder")

    st.write(
        "Create a professional resume using your personal, "
        "education, skills, experience and project details."
    )

    st.markdown("---")

    # =================================================
    # PERSONAL INFORMATION
    # =================================================

    st.subheader("👤 Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")

    with col2:
        phone = st.text_input("Phone")
        location = st.text_input("Location")

    # =================================================
    # PROFESSIONAL SUMMARY
    # =================================================

    st.subheader("📝 Professional Summary")

    summary = st.text_area(
        "Write a short professional summary",
        height=120,
        placeholder=(
            "Example: BCA AI & DS student with experience "
            "in Python, data analysis and AI projects."
        )
    )

    # =================================================
    # SKILLS
    # =================================================

    st.subheader("🛠️ Skills")

    skills_input = st.text_input(
        "Enter skills separated by commas",
        placeholder="Python, C, SQL, HTML, Pandas"
    )

    skills = [
        skill.strip()
        for skill in skills_input.split(",")
        if skill.strip()
    ]

    # =================================================
    # EDUCATION
    # =================================================

    st.subheader("🎓 Education")

    education_input = st.text_area(
        "Education details",
        placeholder=(
            "BCA AI & DS - Poornima University\n"
            "Class 12 - XYZ School"
        )
    )

    education = [
        item.strip()
        for item in education_input.split("\n")
        if item.strip()
    ]

    # =================================================
    # EXPERIENCE
    # =================================================

    st.subheader("💼 Experience")

    experience_input = st.text_area(
        "Experience details",
        placeholder=(
            "Python Developer Intern - ABC Company\n"
            "Data Analyst Intern - XYZ Company"
        )
    )

    experience = [
        item.strip()
        for item in experience_input.split("\n")
        if item.strip()
    ]

    # =================================================
    # PROJECTS
    # =================================================

    st.subheader("🚀 Projects")

    number_of_projects = st.number_input(
        "Number of Projects",
        min_value=0,
        max_value=5,
        value=1,
        step=1
    )

    projects = []

    # Create input fields dynamically for each project
    for i in range(int(number_of_projects)):

        st.markdown(f"**Project {i + 1}**")

        project_name = st.text_input(
            "Project Name",
            key=f"project_name_{i}"
        )

        project_description = st.text_area(
            "Project Description",
            key=f"project_description_{i}"
        )

        if project_name.strip():

            projects.append({
                "name": project_name.strip(),
                "description": project_description.strip()
            })

    # =================================================
    # GENERATE RESUME
    # =================================================

    st.markdown("---")

    if st.button(
        "🚀 Generate Resume",
        type="primary",
        use_container_width=True
    ):

        # Basic validation
        if not name.strip() or not email.strip():

            st.warning(
                "Please enter at least your name and email."
            )

        else:

            # Create structured resume data
            resume_data = create_resume_data(
                name=name,
                email=email,
                phone=phone,
                location=location,
                summary=summary,
                education=education,
                skills=skills,
                experience=experience,
                projects=projects
            )

            # Generate formatted resume
            resume_text = generate_resume_text(
                resume_data
            )

            st.success(
                "Resume generated successfully!"
            )

            # =================================================
            # RESUME PREVIEW
            # =================================================

            st.subheader("📄 Resume Preview")

            st.text_area(
                "Generated Resume",
                value=resume_text,
                height=600
            )

            st.download_button(
                label="⬇️ Download Resume",
                data=resume_text,
                file_name="professional_resume.txt",
                mime="text/plain",
                use_container_width=True
            )
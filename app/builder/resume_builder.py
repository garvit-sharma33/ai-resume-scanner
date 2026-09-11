def create_resume_data(
    name,
    email,
    phone,
    location,
    summary,
    education,
    skills,
    experience,
    projects
):
    """
    Creates a structured dictionary containing all resume information.
    This data will later be used to generate the final resume.
    """

    resume_data = {
        "personal": {
            "name": name,
            "email": email,
            "phone": phone,
            "location": location
        },

        "summary": summary,

        "education": education,

        "skills": skills,

        "experience": experience,

        "projects": projects
    }

    return resume_data


def generate_resume_text(resume_data):
    """
    Converts structured resume data into a professional
    plain-text resume format.
    """

    personal = resume_data["personal"]

    resume = ""

    # Header / Personal Information
    resume += f"{personal['name'].upper()}\n"
    resume += f"{personal['email']} | {personal['phone']} | {personal['location']}\n"
    resume += "=" * 60 + "\n\n"

    # Professional Summary
    if resume_data["summary"]:
        resume += "PROFESSIONAL SUMMARY\n"
        resume += "-" * 60 + "\n"
        resume += resume_data["summary"] + "\n\n"

    # Skills
    if resume_data["skills"]:
        resume += "SKILLS\n"
        resume += "-" * 60 + "\n"
        resume += ", ".join(resume_data["skills"]) + "\n\n"

    # Education
    if resume_data["education"]:
        resume += "EDUCATION\n"
        resume += "-" * 60 + "\n"

        for education in resume_data["education"]:
            resume += f"• {education}\n"

        resume += "\n"

    # Experience
    if resume_data["experience"]:
        resume += "EXPERIENCE\n"
        resume += "-" * 60 + "\n"

        for experience in resume_data["experience"]:
            resume += f"• {experience}\n"

        resume += "\n"

    # Projects
    if resume_data["projects"]:
        resume += "PROJECTS\n"
        resume += "-" * 60 + "\n"

        for project in resume_data["projects"]:
            resume += f"{project['name']}\n"
            resume += f"  {project['description']}\n\n"

    return resume


if __name__ == "__main__":
    resume = create_resume_data(
        name="Garvit Sharma",
        email="garvit@example.com",
        phone="9876543210",
        location="Jaipur, Rajasthan",
        summary="BCA AI & DS student interested in Python and AI.",
        education=[
            "BCA AI & DS - Poornima University"
        ],
        skills=[
            "Python",
            "C",
            "SQL",
            "HTML"
        ],
        experience=[],
        projects=[
            {
                "name": "AI Resume Scanner",
                "description": "AI-based resume analysis and career assistant."
            }
        ]
    )

    print(generate_resume_text(resume))
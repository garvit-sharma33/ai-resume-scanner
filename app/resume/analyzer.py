import json
import re
from app.resume.parser import extract_resume_text


# Load available skills from the external skills database
def load_skills():

    with open("data/skills.json", "r", encoding="utf-8") as file:
        return json.load(file)


# Search the resume text and find skills present in our skill database
def extract_skills(text):

    skills_data = load_skills()
    found_skills = []

    # Check every category and every skill stored in skills.json
    for category, skills in skills_data.items():

        for skill in skills:

            # Create a pattern that matches the complete skill name
            pattern = r"\b" + re.escape(skill) + r"\b"

            # Search the skill in the resume without case sensitivity
            if re.search(pattern, text, re.IGNORECASE):
                found_skills.append(skill)

    return found_skills


# Load education-related terms from the education database
def load_education():

    with open("data/education.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Find education qualifications mentioned in the resume
def extract_education(text):

    education_data = load_education()
    found_education = []

    # Check both degrees and general education keywords
    education_terms = (
        education_data["degrees"]
        + education_data["education_keywords"]
    )

    for term in education_terms:

        # Match the complete term without considering letter case
        pattern = r"\b" + re.escape(term) + r"\b"

        if re.search(pattern, text, re.IGNORECASE):
            found_education.append(term)

    return found_education


# Load experience-related keywords from the experience database
def load_experience():

    with open("data/experience.json", "r", encoding="utf-8") as file:
        return json.load(file)


# Find experience-related information in the resume
def extract_experience(text):

    experience_data = load_experience()
    found_experience = []

    for keyword in experience_data["experience_keywords"]:

        # Search for experience keywords without considering letter case
        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(pattern, text, re.IGNORECASE):
            found_experience.append(keyword)

    return found_experience


# Extract experience-related lines from the resume
def extract_experience_details(text):

    experience_details = []

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Check whether the line contains an experience-related keyword
        for keyword in [
            "Intern",
            "Internship",
            "Developer",
            "Engineer",
            "Analyst",
            "Trainee"
        ]:

            if re.search(r"\b" + re.escape(keyword) + r"\b",
                         line, re.IGNORECASE):

                experience_details.append(line)
                break

    return experience_details

# Extract basic contact information from the resume
def extract_basic_info(text):

    basic_info = {
        "name": "",
        "email": "",
        "phone": ""
    }

    # Find email address using a regular expression
    email_match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )

    if email_match:
        basic_info["email"] = email_match.group()

    # Find a phone number from the resume
    phone_match = re.search(
    r"(?:\+91[\s-]?)?[6-9]\d{9}",
    text
)

    if phone_match:
        basic_info["phone"] = phone_match.group()

    # Use the first non-empty line as a basic name guess
    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        if line and "@" not in line and not re.search(r"\d", line):
            basic_info["name"] = line
            break

    return basic_info


# Detect important sections present in the resume
def detect_sections(text):

    sections = []

    section_keywords = {
        "Skills": ["Skills", "Technical Skills"],
        "Education": ["Education", "Academic Background"],
        "Experience": ["Experience", "Work Experience"],
        "Projects": ["Projects", "Academic Projects", "Personal Projects"]
    }

    for section, keywords in section_keywords.items():

        for keyword in keywords:

            # Check whether the section heading exists in the resume
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text, re.IGNORECASE):
                sections.append(section)
                break

    return sections


# Analyze resume text and extract important information
def analyze_resume(text):

    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)
    basic_info = extract_basic_info(text)
    sections = detect_sections(text)
    experience_details = extract_experience_details(text)

    resume_data = {

        "name": basic_info["name"],
        "email": basic_info["email"],
        "phone": basic_info["phone"],
        "skills": skills,
        "education": education,
        "experience": experience,
        "experience_details": experience_details,
        "sections": sections,
        "total_skills": len(skills)
        
    }

    return resume_data

# Test the complete resume analysis pipeline
if __name__ == "__main__":

    file_path = "test_resume/test_resume.pdf"

    resume_text = extract_resume_text(file_path)

    if resume_text:

        result = analyze_resume(resume_text)

        print("\n----- RESUME ANALYSIS -----\n")

        print("Name:")
        print(result["name"])

        print("\nEmail:")
        print(result["email"])

        print("\nPhone:")
        print(result["phone"])

        print("Skills:")
        print(result["skills"])

        print("\nEducation:")
        print(result["education"])

        print("\nExperience:")
        print(result["experience"])

        print("\nExperience Details:")
        print(result["experience_details"])

        print("\nSections:")
        print(result["sections"])

        print("\nTotal Skills:")
        print(result["total_skills"])
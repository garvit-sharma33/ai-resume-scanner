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


    # Calculate an overall resume score out of 100
def calculate_resume_score(skills, education, experience_details, sections):

    score = 0

    # Skills score: maximum 40 marks
    skill_count = len(skills)

    if skill_count >= 10:
        score += 40
    elif skill_count >= 7:
        score += 32
    elif skill_count >= 4:
        score += 24
    elif skill_count >= 1:
        score += 12

    # Education score: maximum 20 marks
    if education:
        score += 20

    # Experience score: maximum 20 marks
    if experience_details:
        score += 20

    # Section score: 5 marks for each important section
    important_sections = [
        "Skills",
        "Education",
        "Experience",
        "Projects"
    ]

    for section in important_sections:
        if section in sections:
            score += 5

    return score


# Calculate category-wise resume score
def calculate_score_breakdown(skills, education, experience_details, sections):

    breakdown = {
        "skills_score": 0,
        "education_score": 0,
        "experience_score": 0,
        "sections_score": 0
    }

    # Skills score
    skill_count = len(skills)

    if skill_count >= 10:
        breakdown["skills_score"] = 40
    elif skill_count >= 7:
        breakdown["skills_score"] = 32
    elif skill_count >= 4:
        breakdown["skills_score"] = 24
    elif skill_count >= 1:
        breakdown["skills_score"] = 12

    # Education score
    if education:
        breakdown["education_score"] = 20

    # Experience score
    if experience_details:
        breakdown["experience_score"] = 20

    # Resume sections score
    important_sections = [
        "Skills",
        "Education",
        "Experience",
        "Projects"
    ]

    for section in important_sections:
        if section in sections:
            breakdown["sections_score"] += 5

    return breakdown


# Convert the resume score into a readable rating
def get_resume_rating(score):

    if score >= 90:
        return "Excellent"

    elif score >= 75:
        return "Good"

    elif score >= 60:
        return "Average"

    elif score >= 40:
        return "Needs Improvement"

    else:
        return "Poor"


# Load job roles and their required/preferred skills
def load_job_roles():

    with open("data/job_roles.json", "r", encoding="utf-8") as file:
        return json.load(file)


# Compare resume skills with job role skills and calculate match percentage
def detect_job_roles(skills):

    job_roles = load_job_roles()
    job_matches = []

    for role, requirements in job_roles.items():

        required_skills = requirements["required"]
        preferred_skills = requirements["preferred"]

        # Count matching required skills
        required_matches = 0

        for skill in required_skills:
            if skill in skills:
                required_matches += 1

        # Count matching preferred skills
        preferred_matches = 0

        for skill in preferred_skills:
            if skill in skills:
                preferred_matches += 1

        total_skills = len(required_skills) + len(preferred_skills)
        matched_skills = required_matches + preferred_matches

        # Calculate overall role match percentage
        if total_skills > 0:
            match_percentage = round(
                (matched_skills / total_skills) * 100
            )
        else:
            match_percentage = 0

        # Only keep roles with a meaningful skill match
        if match_percentage >= 30:

            job_matches.append({
                "role": role,
                "match_percentage": match_percentage
            })


    # Show highest matching roles first
    job_matches.sort(
        key=lambda item: item["match_percentage"],
        reverse=True
    )

    return job_matches


# Find skills that are useful for recommended job roles but missing from the resume
def find_skill_gaps(skills, job_matches):

    job_roles = load_job_roles()
    skill_gaps = {}

    for job in job_matches:

        role = job["role"]
        match_percentage = job["match_percentage"]

        required_skills = job_roles[role]["required"]
        preferred_skills = job_roles[role]["preferred"]

        missing_skills = []

        # Check missing required skills
        for skill in required_skills:
            if skill not in skills:
                missing_skills.append(skill)

        # Check missing preferred skills
        for skill in preferred_skills:
            if skill not in skills:
                missing_skills.append(skill)

        skill_gaps[role] = {
            "match_percentage": match_percentage,
            "missing_skills": missing_skills
        }

    return skill_gaps


# Load learning suggestions for different skills
def load_skill_suggestions():

    with open("data/skill_suggestions.json", "r", encoding="utf-8") as file:
        return json.load(file)


# Generate learning suggestions for missing skills
def generate_skill_suggestions(skill_gaps):

    suggestions_data = load_skill_suggestions()
    suggestions = {}

    for role, data in skill_gaps.items():

        role_suggestions = []

        for skill in data["missing_skills"]:

            if skill in suggestions_data:

                role_suggestions.append({
                    "skill": skill,
                    "suggestion": suggestions_data[skill]
                })

        suggestions[role] = role_suggestions

    return suggestions

# Analyze resume text and extract important information
def analyze_resume(text):

    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)
    basic_info = extract_basic_info(text)
    sections = detect_sections(text)
    experience_details = extract_experience_details(text)
    score = calculate_resume_score(
            skills,
            education,
            experience_details,
            sections
        )

    score_breakdown = calculate_score_breakdown(
            skills,
            education,
            experience_details,
            sections
        )

    rating = get_resume_rating(score)
    job_matches = detect_job_roles(skills)
    skill_gaps = find_skill_gaps(skills, job_matches)
    suggestions = generate_skill_suggestions(skill_gaps)

    resume_data = {

        "name": basic_info["name"],
        "email": basic_info["email"],
        "phone": basic_info["phone"],
        "skills": skills,
        "education": education,
        "experience": experience,
        "experience_details": experience_details,
        "resume_score": score,
        "score_breakdown": score_breakdown,
        "resume_rating": rating,
        "job_matches": job_matches,
        "skill_gaps": skill_gaps,
        "skill_suggestions": suggestions,
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

        print("\nResume Score:")
        print(result["resume_score"], "/ 100")

        print("\nScore Breakdown:")
        print(result["score_breakdown"])

        print("\nResume Rating:")
        print(result["resume_rating"])

        print("\nJob Role Matches:")

        for job in result["job_matches"]:
            print(
                job["role"],
                "->",
                job["match_percentage"],
                "%"
            )

        print("\nSkill Gaps:")

        for role, data in result["skill_gaps"].items():

            print(
                role,
                "-> Missing:",
                data["missing_skills"]
            )

        print("\nSkill Improvement Suggestions:")

        for role, suggestions in result["skill_suggestions"].items():

            print("\n" + role)

            for item in suggestions:

                print(
                    "-",
                    item["skill"],
                    ":",
                    item["suggestion"]
                )
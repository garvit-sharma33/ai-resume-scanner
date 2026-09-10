import json

from app.resume.parser import extract_resume_text
from app.resume.analyzer import analyze_resume

# Load career roadmap data
def load_career_roadmaps():

    with open(
        "data/career_roadmaps.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# Find missing skills for a selected career
def find_career_skill_gaps(resume_skills, career_skills):

    resume_skill_set = {
        skill.strip().lower()
        for skill in resume_skills
    }

    missing_skills = []

    for skill in career_skills:

        if skill.strip().lower() not in resume_skill_set:
            missing_skills.append(skill)

    return missing_skills


# Calculate how ready the user is for a career
def calculate_career_readiness(
    resume_skills,
    career_skills
):

    if not career_skills:
        return 0

    resume_skill_set = {
        skill.strip().lower()
        for skill in resume_skills
    }

    matched_skills = 0

    for skill in career_skills:

        if skill.strip().lower() in resume_skill_set:
            matched_skills += 1

    readiness = round(
        (matched_skills / len(career_skills)) * 100
    )

    return readiness


# Generate complete roadmap for a career
def generate_career_roadmap(
    resume_skills,
    career_name
):

    roadmaps = load_career_roadmaps()

    if career_name not in roadmaps:
        return {}

    career_data = roadmaps[career_name]

    career_skills = career_data["skills"]

    missing_skills = find_career_skill_gaps(
        resume_skills,
        career_skills
    )

    readiness = calculate_career_readiness(
        resume_skills,
        career_skills
    )

    return {
        "career": career_name,
        "required_skills": career_skills,
        "current_skills": resume_skills,
        "missing_skills": missing_skills,
        "readiness": readiness,
        "roadmap_steps": career_data["steps"]
    }


# Predict suitable careers based on resume skills
def predict_career_paths(resume_skills):

    roadmaps = load_career_roadmaps()

    career_matches = []

    for career_name, career_data in roadmaps.items():

        career_skills = career_data["skills"]

        readiness = calculate_career_readiness(
            resume_skills,
            career_skills
        )

        if readiness > 0:

            career_matches.append({
                "career": career_name,
                "match_percentage": readiness
            })

    # Highest matching career appears first
    career_matches.sort(
        key=lambda item: item["match_percentage"],
        reverse=True
    )

    return career_matches


# Test Career Engine
if __name__ == "__main__":

    test_resume_skills = [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Git",
        "GitHub"
    ]

    print("\n----- CAREER PREDICTION -----\n")

    careers = predict_career_paths(
        test_resume_skills
    )

    for career in careers:

        print(
            career["career"],
            "→",
            career["match_percentage"],
            "%"
        )

    print("\n----- PYTHON DEVELOPER ROADMAP -----\n")

    roadmap = generate_career_roadmap(
        test_resume_skills,
        "Python Developer"
    )

    print("Career:", roadmap["career"])
    print("Readiness:", roadmap["readiness"], "%")
    print("Current Skills:", roadmap["current_skills"])
    print("Missing Skills:", roadmap["missing_skills"])

    print("\nRoadmap:")

    for step in roadmap["roadmap_steps"]:
        print("-", step)



# Calculate overall job readiness score
def calculate_job_readiness(
    resume_score,
    career_readiness
):

    # Resume quality contributes 40%
    resume_part = resume_score * 0.40

    # Career skill readiness contributes 60%
    career_part = career_readiness * 0.60

    readiness_score = round(
        resume_part + career_part
    )

    return readiness_score


# Convert career readiness percentage into a readable recommendation
def get_career_recommendation(readiness):

    if readiness >= 80:
        return "Excellent Career Fit"

    elif readiness >= 60:
        return "Strong Career Fit"

    elif readiness >= 40:
        return "Moderate Career Fit"

    else:
        return "Beginner Level"


# Test complete Career Engine with actual resume
if __name__ == "__main__":

    resume_path = "test_resume/test_resume.pdf"

    # Extract resume text
    resume_text = extract_resume_text(resume_path)

    if not resume_text:
        print("Resume text could not be extracted.")
        exit()

    # Analyze resume
    resume_data = analyze_resume(resume_text)

    resume_skills = resume_data.get("skills", [])
    resume_score = resume_data.get("resume_score", 0)

    print("\n----- RESUME INFORMATION -----\n")

    print("Resume Score:", resume_score)
    print("Resume Skills:", resume_skills)

    if not resume_skills:
        print("\nNo skills detected in resume.")
        exit()

    # Predict career paths
    print("\n----- CAREER PREDICTION -----\n")

    careers = predict_career_paths(resume_skills)

    for career in careers[:5]:

        print(
            career["career"],
            "→",
            career["match_percentage"],
            "%"
        )

    # Generate roadmap for the best career
    if careers:

        best_career = careers[0]["career"]

        roadmap = generate_career_roadmap(
            resume_skills,
            best_career
        )

        career_readiness = roadmap["readiness"]

        # Calculate overall job readiness
        job_readiness = calculate_job_readiness(
            resume_score,
            career_readiness
        )

        print("\n----- RECOMMENDED CAREER -----\n")

        print("Career:", best_career)

        print(
            "Career Readiness:",
            career_readiness,
            "%"
        )

        print(
            "Overall Job Readiness:",
            job_readiness,
            "%"
        )

        print(
            "Career Recommendation:",
            get_career_recommendation(career_readiness)
        )

        print(
            "Missing Skills:",
            roadmap["missing_skills"]
        )

        print("\n----- CAREER ROADMAP -----\n")

        for step in roadmap["roadmap_steps"]:

            print("-", step)
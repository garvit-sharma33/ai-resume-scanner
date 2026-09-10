import requests
import json
import re

from app.resume.parser import extract_resume_text
from app.resume.analyzer import analyze_resume, load_skill_suggestions


# Fetch jobs from Himalayas public API
def fetch_jobs(limit=20):

    url = "https://himalayas.app/jobs/api"

    try:
        response = requests.get(
            url,
            params={"limit": limit},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data.get("jobs", [])

    except requests.RequestException as error:
        print(f"Error while fetching jobs: {error}")
        return []


# Load all skills from skills.json
def load_skills():

    with open("data/skills.json", "r", encoding="utf-8") as file:
        skills_data = json.load(file)

    all_skills = []

    for skills in skills_data.values():
        all_skills.extend(skills)

    # Remove duplicate skills
    return list(dict.fromkeys(all_skills))


# Detect skills from job title and description
def extract_job_skills(job):

    all_skills = load_skills()

    job_text = (
        job.get("title", "") + " " +
        job.get("description", "")
    )

    required_skills = []
    preferred_skills = []

    for skill in all_skills:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, job_text, re.IGNORECASE):
            required_skills.append(skill)

    # Remove duplicate skills
    required_skills = list(dict.fromkeys(required_skills))

    # For now, keep preferred skills separate but empty.
    # This avoids incorrect classification from inconsistent job descriptions.
    preferred_skills = []

    return {
        "required": required_skills,
        "preferred": preferred_skills
    }


# Convert API data into clean project data
def clean_job_data(jobs):

    cleaned_jobs = []

    for job in jobs:

        skill_data = extract_job_skills(job)

        cleaned_job = {
            "title": job.get("title", "Unknown"),
            "company": job.get("companyName", "Unknown"),
            "location": job.get("location", "Remote"),
            "type": job.get("employmentType", "Unknown"),

            "required_skills": skill_data["required"],
            "preferred_skills": skill_data["preferred"],

            "apply_link": job.get("applicationLink", "")
        }

        cleaned_jobs.append(cleaned_job)

    return cleaned_jobs


# Calculate job match percentage
def calculate_job_match(
    resume_skills,
    required_skills,
    preferred_skills
):

    resume_skill_set = {
        skill.strip().lower()
        for skill in resume_skills
    }

    required_skill_set = {
        skill.strip().lower()
        for skill in required_skills
    }

    preferred_skill_set = {
        skill.strip().lower()
        for skill in preferred_skills
    }

    matched_required = (
        resume_skill_set.intersection(required_skill_set)
    )

    matched_preferred = (
        resume_skill_set.intersection(preferred_skill_set)
    )

    # Required skills carry 70% importance
    if required_skill_set:

        required_score = (
            len(matched_required) /
            len(required_skill_set)
        ) * 70

    else:
        required_score = 70

    # Preferred skills carry 30% importance
    if preferred_skill_set:

        preferred_score = (
            len(matched_preferred) /
            len(preferred_skill_set)
        ) * 30

    else:
        preferred_score = 30

    match_percentage = round(
        required_score + preferred_score
    )

    matched_skills = sorted(
        matched_required.union(matched_preferred)
    )

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "matched_required": sorted(matched_required),
        "matched_preferred": sorted(matched_preferred)
    }


# Convert percentage into readable label
def get_match_label(match_percentage):

    if match_percentage >= 80:
        return "Excellent Match"

    elif match_percentage >= 60:
        return "Strong Match"

    elif match_percentage >= 40:
        return "Good Match"

    else:
        return "Low Match"


# Find missing required and preferred skills
def find_job_skill_gaps(
    resume_skills,
    required_skills,
    preferred_skills
):

    resume_skill_set = {
        skill.strip().lower()
        for skill in resume_skills
    }

    missing_required = []
    missing_preferred = []

    for skill in required_skills:

        if skill.strip().lower() not in resume_skill_set:
            missing_required.append(skill)

    for skill in preferred_skills:

        if skill.strip().lower() not in resume_skill_set:
            missing_preferred.append(skill)

    return {
        "missing_required": list(
            dict.fromkeys(missing_required)
        ),

        "missing_preferred": list(
            dict.fromkeys(missing_preferred)
        )
    }


# Generate learning suggestions for missing skills
def generate_learning_suggestions(missing_skills):

    suggestions_data = load_skill_suggestions()

    suggestions = []

    # Show suggestions for maximum two missing skills
    for skill in missing_skills[:2]:

        if skill in suggestions_data:

            suggestions.append({
                "skill": skill,
                "suggestion": suggestions_data[skill]
            })

    return suggestions


# Rank jobs according to resume match
def rank_jobs(resume_skills, jobs):

    ranked_jobs = []

    for job in jobs:

        match_result = calculate_job_match(
            resume_skills,
            job["required_skills"],
            job["preferred_skills"]
        )

        gap_result = find_job_skill_gaps(
            resume_skills,
            job["required_skills"],
            job["preferred_skills"]
        )

        all_missing_skills = (
            gap_result["missing_required"] +
            gap_result["missing_preferred"]
        )

        job_result = job.copy()

        job_result["match_percentage"] = (
            match_result["match_percentage"]
        )

        job_result["matched_skills"] = (
            match_result["matched_skills"]
        )

        job_result["matched_required"] = (
            match_result["matched_required"]
        )

        job_result["matched_preferred"] = (
            match_result["matched_preferred"]
        )

        job_result["missing_required"] = (
            gap_result["missing_required"]
        )

        job_result["missing_preferred"] = (
            gap_result["missing_preferred"]
        )

        job_result["learning_suggestions"] = (
            generate_learning_suggestions(
                all_missing_skills
            )
        )

        job_result["match_label"] = get_match_label(
            job_result["match_percentage"]
        )

        # Keep only jobs having at least one matched skill
        if job_result["matched_skills"]:
            ranked_jobs.append(job_result)

    ranked_jobs.sort(
        key=lambda job: job["match_percentage"],
        reverse=True
    )

    return ranked_jobs


# Test complete job recommendation pipeline
if __name__ == "__main__":

    resume_path = "test_resume/test_resume.pdf"

    # Extract text from resume
    resume_text = extract_resume_text(resume_path)

    if not resume_text:
        print("Resume text could not be extracted.")
        exit()

    # Analyze resume text
    resume_data = analyze_resume(resume_text)

    resume_skills = resume_data.get("skills", [])

    print("\n----- RESUME SKILLS -----\n")
    print(resume_skills)

    if not resume_skills:
        print("\nNo skills were detected in the resume.")
        exit()

    # Fetch live jobs
    jobs = fetch_jobs()

    if not jobs:
        print("\nNo jobs found.")
        exit()

    # Clean job data
    cleaned_jobs = clean_job_data(jobs)

    # Rank jobs
    ranked_jobs = rank_jobs(
        resume_skills,
        cleaned_jobs
    )

    print("\n----- TOP RECOMMENDED JOBS -----\n")

    for job in ranked_jobs[:10]:

        print("Job:", job["title"])
        print("Company:", job["company"])

        print("Required Skills:", job["required_skills"])
        print("Preferred Skills:", job["preferred_skills"])

        print("Matched Skills:", job["matched_skills"])
        print("Matched Required:", job["matched_required"])
        print("Matched Preferred:", job["matched_preferred"])

        print("Missing Required:", job["missing_required"])
        print("Missing Preferred:", job["missing_preferred"])

        print(
            "Learning Suggestions:",
            job["learning_suggestions"]
        )

        print("Match:", job["match_percentage"], "%")
        print("Recommendation:", job["match_label"])

        print("Apply:", job["apply_link"])

        print("-" * 60)
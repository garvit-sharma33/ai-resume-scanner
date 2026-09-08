import requests
import json
import re

from app.resume.parser import extract_resume_text
from app.resume.analyzer import analyze_resume


# Fetch job listings from the Himalayas public API
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


# Load all skills used by our resume analysis system
def load_skills():

    with open("data/skills.json", "r", encoding="utf-8") as file:
        skills_data = json.load(file)

    all_skills = []

    for skills in skills_data.values():
        all_skills.extend(skills)

    return all_skills


# Find known project skills inside a job title and description
def extract_job_skills(job):

    all_skills = load_skills()

    job_text = (
        job.get("title", "") + " " +
        job.get("description", "")
    )

    found_skills = []

    for skill in all_skills:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, job_text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


# Convert raw API data into the format required by our project
def clean_job_data(jobs):

    cleaned_jobs = []

    for job in jobs:

        cleaned_job = {
            "title": job.get("title", "Unknown"),
            "company": job.get("companyName", "Unknown"),
            "location": job.get("location", "Remote"),
            "type": job.get("employmentType", "Unknown"),
            "skills": extract_job_skills(job),
            "apply_link": job.get("applicationLink", "")
        }

        cleaned_jobs.append(cleaned_job)

    return cleaned_jobs


# Convert match percentage into a simple recommendation label
def get_match_label(match_percentage):

    if match_percentage >= 80:
        return "Excellent Match"

    elif match_percentage >= 60:
        return "Strong Match"

    elif match_percentage >= 40:
        return "Good Match"

    else:
        return "Low Match"

# Compare resume skills with job skills and calculate the match
def calculate_job_match(resume_skills, job_skills):

    if not job_skills:
        return {
            "match_percentage": 0,
            "matched_skills": []
        }

    # Lowercase sets make the comparison case-insensitive
    resume_skill_set = {
        skill.strip().lower()
        for skill in resume_skills
    }

    job_skill_set = {
        skill.strip().lower()
        for skill in job_skills
    }

    matched_skills = resume_skill_set.intersection(job_skill_set)

    match_percentage = round(
        (len(matched_skills) / len(job_skill_set)) * 100
    )

    return {
        "match_percentage": match_percentage,
        "matched_skills": sorted(matched_skills)
    }


# Rank jobs from highest skill match to lowest
def rank_jobs(resume_skills, jobs):

    ranked_jobs = []

    for job in jobs:

        match_result = calculate_job_match(
            resume_skills,
            job["skills"]
        )

        job_result = job.copy()

        job_result["match_percentage"] = (
            match_result["match_percentage"]
        )

        job_result["matched_skills"] = (
            match_result["matched_skills"]
        )

        job_result["match_label"] = get_match_label(
            job_result["match_percentage"]
        )

        # Ignore jobs that have no skill match
        if job_result["match_percentage"] > 0:
            ranked_jobs.append(job_result)

    ranked_jobs.sort(
        key=lambda job: job["match_percentage"],
        reverse=True
    )

    return ranked_jobs


# Run the complete resume-to-job recommendation pipeline
if __name__ == "__main__":

    # Resume file used for testing
    resume_path = "test_resume/test_resume.pdf"

    # Extract and clean text before sending it to the analyzer
    resume_text = extract_resume_text(resume_path)

    if not resume_text:
        print("Resume text could not be extracted.")
        exit()

    # Analyze the cleaned resume text and get its skills
    resume_data = analyze_resume(resume_text)

    resume_skills = resume_data.get("skills", [])

    print("\n----- RESUME SKILLS -----\n")
    print(resume_skills)

    if not resume_skills:
        print("\nNo skills were detected in the resume.")
        exit()

    # Fetch and process jobs from the API
    jobs = fetch_jobs()

    if not jobs:
        print("\nNo jobs found.")
        exit()

    cleaned_jobs = clean_job_data(jobs)

    # Match the actual resume skills with every available job
    ranked_jobs = rank_jobs(
        resume_skills,
        cleaned_jobs
    )

    print("\n----- TOP RECOMMENDED JOBS -----\n")

for job in ranked_jobs[:10]:

    print("Job:", job["title"])
    print("Company:", job["company"])
    print("Job Skills:", job["skills"])
    print("Matched Skills:", job["matched_skills"])
    print("Match:", job["match_percentage"], "%")
    print("Recommendation:", job["match_label"])
    print("Apply:", job["apply_link"])
    print("-" * 60)
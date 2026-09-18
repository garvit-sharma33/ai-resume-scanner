import os

from dotenv import load_dotenv
from google import genai


# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please check your .env file."
    )


client = genai.Client(api_key=API_KEY)


def ask_gemini(prompt):
    """
    Send a prompt to Gemini and return the generated response.
    """

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text


def generate_career_advice(
    skills,
    career,
    missing_skills
):
    """
    Generate personalized career advice
    based on resume skills and career gaps.
    """

    prompt = f"""
You are an AI career assistant.

Candidate's skills:
{skills}

Recommended career:
{career}

Missing skills:
{missing_skills}

Analyze the candidate and provide practical,
professional and beginner-friendly career advice.

Include:

1. Current strengths
2. Skills to improve
3. What to learn next
4. A short action plan
5. How the candidate can become job-ready

Keep the response clear, practical and concise.

Do not make unrealistic promises.
"""

    return ask_gemini(prompt)
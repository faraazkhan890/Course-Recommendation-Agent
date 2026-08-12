import argparse
import json
import os
from dotenv import load_dotenv
from groq import Groq

# Load Environment Variables from .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("\n[ERROR] GROQ_API_KEY is missing! Check your .env file.")
    exit(1)

client = Groq(api_key=api_key)

# HARDCODED DATASETS (Bypasses JSON file parsing errors)
COURSES = [
    {
        "id": "CS101",
        "title": "Programming Fundamentals with Python",
        "prerequisites": [],
        "skills_learned": ["Python Basics", "Basic Logic"],
    },
    {
        "id": "CS102",
        "title": "Data Structures & Algorithms in Python",
        "prerequisites": ["CS101"],
        "skills_learned": ["Data Structures", "Algorithms"],
    },
    {
        "id": "WEB101",
        "title": "Full-Stack Web Development with Django & MySQL",
        "prerequisites": ["CS101"],
        "skills_learned": ["Django", "REST APIs", "MySQL"],
    },
    {
        "id": "AI101",
        "title": "Applied Machine Learning & Computer Vision",
        "prerequisites": ["CS101", "CS102"],
        "skills_learned": ["Machine Learning", "OpenCV", "YOLOv8"],
    },
]

PROFILES = [
    {
        "id": "STU_001",
        "name": "Mohammad Faraaz Khan",
        "current_background": "Final-Year B.Tech ECE Student",
        "known_skills": ["Python Basics", "Basic Logic"],
        "career_goal": "Full-Stack AI Developer (Django & Computer Vision)",
    },
    {
        "id": "STU_002",
        "name": "Ananya Sharma",
        "current_background": "Non-CS Undergraduate",
        "known_skills": [],
        "career_goal": "Python Developer",
    },
    {
        "id": "STU_003",
        "name": "Rahul Verma",
        "current_background": "Software Developer",
        "known_skills": ["Python Basics", "Basic Logic", "CS101", "CS102"],
        "career_goal": "AI Research Engineer",
    },
]


def validate_prerequisites(profile, courses):
    known_items = set(profile.get("known_skills", []))

    # Map completed skills back to course IDs so prerequisites clear correctly
    for course in courses:
        if all(skill in known_items for skill in course.get("skills_learned", [])):
            known_items.add(course["id"])

    eligible_courses = []
    locked_courses = []

    for course in courses:
        prereqs = course.get("prerequisites", [])
        if not prereqs or all(p in known_items for p in prereqs):
            eligible_courses.append(course["id"])
        else:
            missing_prereqs = [p for p in prereqs if p not in known_items]
            locked_courses.append({"course_id": course["id"], "missing": missing_prereqs})

    return eligible_courses, locked_courses


def run_course_recommendation_agent(profile, courses):
    eligible_ids, locked_info = validate_prerequisites(profile, courses)

    system_prompt = (
        "You are an expert Academic & Career Path AI Advisor.\n"
        "Your task is to analyze a student's profile and a course catalog to build an ordered learning path.\n"
        "STRICT RULES:\n"
        "1. Never recommend a course unless its prerequisites are completed or in known_skills.\n"
        "2. Output ONLY valid JSON matching this schema:\n"
        "{\n"
        '  "student_id": "string",\n'
        '  "student_name": "string",\n'
        '  "career_goal": "string",\n'
        '  "recommended_learning_path": [\n'
        "    {\n"
        '      "step": 1,\n'
        '      "course_id": "string",\n'
        '      "course_title": "string",\n'
        '      "rationale": "string"\n'
        "    }\n"
        "  ],\n"
        '  "overall_summary": "string"\n'
        "}\n"
    )

    user_prompt = f"""
    Student Profile: {json.dumps(profile, indent=2)}
    Available Course Catalog: {json.dumps(courses, indent=2)}
    Pre-Calculated Prerequisite Check:
    - Directly Eligible Course IDs: {eligible_ids}
    - Currently Locked Courses: {locked_info}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)


def main():
    parser = argparse.ArgumentParser(description="Run Course Recommendation AI Agent")
    parser.add_argument(
        "--profile_index",
        type=int,
        default=0,
        help="Index of profile (0, 1, 2)",
    )
    args = parser.parse_args()

    if args.profile_index < 0 or args.profile_index >= len(PROFILES):
        print(f"\n[ERROR] Invalid profile index {args.profile_index}. Choose 0, 1, or 2.")
        return

    selected_profile = PROFILES[args.profile_index]
    print(f"\n[INFO] Running Agent for Student: {selected_profile['name']}...")

    result = run_course_recommendation_agent(selected_profile, COURSES)

    output_filename = f"sample_output_profile_{args.profile_index + 1}.json"
    with open(output_filename, "w") as f:
        json.dump(result, f, indent=2)

    print("\n--- RECOMMENDED LEARNING PATH OUTPUT ---")
    print(json.dumps(result, indent=2))
    print(f"\n[SUCCESS] Result saved to '{output_filename}'")


if __name__ == "__main__":
    main() 

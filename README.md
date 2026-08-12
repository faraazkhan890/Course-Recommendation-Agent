# Course Recommendation AI Agent

An AI agent that takes a student's profile (known skills, background, career goal) and a course catalog to output a personalized, prerequisite-validated step-by-step learning path.

---

## 📌 Core Capability Statement
> "My agent takes a student profile and a course catalog and produces a prerequisite-validated, ordered learning path with step-by-step reasoning."

---

## 🛠️ How It Works

1. *Input Loading:* Reads course data (courses.json) and student profiles (profiles.json).
2. *Prerequisite Check:* Programmatically checks which courses are unlocked based on the student's existing skills to prevent hallucination.
3. *LLM Path Optimization:* Sends the profile and course data to *Llama-3.3-70B* via Groq API to construct an ordered learning path with clear rationale in structured JSON format.
4. *Output Generation:* Displays the result in the terminal and saves sample JSON output files.

---

## 🚀 Setup & Execution Instructions

1. *Clone the Repository:*
   ```bash
   git clone [https://github.com/faraazkhan890/Course-Recommendation-Agent.git](https://github.com/faraazkhan890/Course-Recommendation-Agent.git)
   cd Course-Recommendation-Agent
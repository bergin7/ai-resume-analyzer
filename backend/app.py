from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import re


app = FastAPI()


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "message": "Welcome to AI Resume Analyzer"
    }


@app.post("/analyze")
async def analyze_resume(

    file: UploadFile = File(...),

    job_description: str = Form(...)

):

    # -----------------------------
    # 1. EXTRACT TEXT FROM RESUME
    # -----------------------------

    resume_text = ""

    with pdfplumber.open(file.file) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:

                resume_text += text + "\n"


    resume_text_lower = resume_text.lower()

    job_description_lower = job_description.lower()


    # -----------------------------
    # 2. SKILL MATCHING
    # -----------------------------

    skills = [

        "python",
        "java",
        "c++",
        "sql",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "data science",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "fastapi",
        "flask",
        "django",
        "react",
        "javascript",
        "html",
        "css",
        "mongodb",
        "docker",
        "git",
        "github",
        "aws",
        "azure"

    ]


    required_skills = [

        skill

        for skill in skills

        if skill in job_description_lower

    ]


    matched_skills = [

        skill

        for skill in required_skills

        if skill in resume_text_lower

    ]


    missing_skills = [

        skill

        for skill in required_skills

        if skill not in resume_text_lower

    ]


    # -----------------------------
    # 3. SKILL SCORE
    # -----------------------------

    if required_skills:

        skill_score = (

            len(matched_skills)

            / len(required_skills)

        ) * 100

    else:

        skill_score = 0


    # -----------------------------
    # 4. SECTION ANALYSIS
    # -----------------------------

    sections = [

        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
        "summary"

    ]


    sections_found = [

        section

        for section in sections

        if section in resume_text_lower

    ]


    missing_sections = [

        section

        for section in sections

        if section not in resume_text_lower

    ]


    # -----------------------------
    # 5. SECTION SCORE
    # -----------------------------

    section_score = (

        len(sections_found)

        / len(sections)

    ) * 100


    # -----------------------------
    # 6. KEYWORD MATCHING
    # -----------------------------

    job_words = set(

        re.findall(

            r"\b[a-zA-Z]{4,}\b",

            job_description_lower

        )

    )


    resume_words = set(

        re.findall(

            r"\b[a-zA-Z]{4,}\b",

            resume_text_lower

        )

    )


    common_keywords = job_words.intersection(

        resume_words

    )


    if job_words:

        keyword_score = (

            len(common_keywords)

            / len(job_words)

        ) * 100

    else:

        keyword_score = 0


    # -----------------------------
    # 7. RESUME QUALITY SCORE
    # -----------------------------

    quality_score = 100

    quality_issues = []


    if len(resume_text) < 500:

        quality_score -= 30

        quality_issues.append(

            "Resume content is too short."

        )


    if len(resume_text) > 10000:

        quality_score -= 10

        quality_issues.append(

            "Resume may contain too much information."

        )


    if "@" not in resume_text:

        quality_score -= 20

        quality_issues.append(

            "Email address may be missing."

        )


    if len(resume_text) < 1000:

        quality_issues.append(

            "Resume content appears short."

        )


    # -----------------------------
    # 8. RESUME IMPROVEMENT SUGGESTIONS
    # -----------------------------

    suggestions = []


    if missing_skills:

        suggestions.append(

            "Consider adding these relevant skills: "

            + ", ".join(missing_skills)

        )


    if missing_sections:

        suggestions.append(

            "Consider adding these resume sections: "

            + ", ".join(missing_sections)

        )


    if keyword_score < 50:

        suggestions.append(

            "Use more relevant keywords from the job description."

        )


    # Check for action words

    action_words = [

        "developed",
        "built",
        "designed",
        "implemented",
        "created",
        "optimized",
        "managed",
        "analyzed"

    ]


    has_action_word = any(

        word in resume_text_lower

        for word in action_words

    )


    if not has_action_word:

        suggestions.append(

            "Use strong action words such as Developed, Built, Designed, Implemented, and Optimized."

        )


    # Check measurable achievements

    numbers = re.findall(

        r"\b\d+%?\b",

        resume_text

    )


    if len(numbers) < 3:

        suggestions.append(

            "Add measurable achievements such as accuracy, performance improvement, or project results."

        )


    # Check project descriptions

    if "projects" in resume_text_lower:

        suggestions.append(

            "Make sure each project explains the technology used and your specific contribution."

        )


    if len(resume_text) < 1000:

        suggestions.append(

            "Your resume content appears short. Add relevant projects, skills, education, or achievements."

        )


    # -----------------------------
    # 9. FINAL ATS SCORE
    # -----------------------------

    ats_score = (

        skill_score * 0.50

        + section_score * 0.20

        + keyword_score * 0.20

        + quality_score * 0.10

    )


    ats_score = round(ats_score)


    # -----------------------------
    # 10. RETURN RESULTS
    # -----------------------------

    return {

        "filename": file.filename,

        "ats_score": ats_score,

        "skill_score": round(skill_score),

        "section_score": round(section_score),

        "keyword_score": round(keyword_score),

        "quality_score": round(quality_score),

        "required_skills": required_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "sections_found": sections_found,

        "missing_sections": missing_sections,

        "suggestions": suggestions,

        "quality_issues": quality_issues

    }
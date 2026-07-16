skills = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "docker",
    "aws",
    "azure",
    "mongodb",
    "fastapi",
    "react",
    "node.js"
]


def extract_skills(text):
    found_skills = []

    text = text.lower()

    for skill in skills:
        if skill in text:
            found_skills.append(skill)

    return found_skills


resume_text = """
I know Python, SQL, Pandas and Machine Learning.
"""

result = extract_skills(resume_text)

print(result)

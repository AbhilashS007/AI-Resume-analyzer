import streamlit as st
import pdfplumber
import pandas as pd


def show_skill_list(skills, empty_message):
    if skills:
        st.markdown(
            " ".join(f"`{skill}`" for skill in skills)
        )
    else:
        st.info(empty_message)

# ----------------------------------
# Extract text from PDF
# ----------------------------------

def extract_text(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

    return text.lower()


# ----------------------------------
# Extract skills
# ----------------------------------

def extract_skills(text):

    skills_df = pd.read_csv("skills.csv")

    skills_list = skills_df["skill"].tolist()

    found_skills = []

    for skill in skills_list:

        if skill.lower() in text:

            found_skills.append(skill)

    return found_skills


# ----------------------------------
# Job Role Skills
# ----------------------------------

job_roles = {

    "Data Analyst": [

        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Data Analysis"

    ],

    "Web Developer": [

        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js"

    ],

    "Full Stack Developer": [

        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "MongoDB",
        "Git"

    ],

    "Machine Learning Engineer": [

        "Python",
        "Machine Learning",
        "Deep Learning",
        "SQL"

    ]
}


# ----------------------------------
# Match Score
# ----------------------------------

def calculate_score(found_skills, required_skills):

    matched = []

    missing = []

    for skill in required_skills:

        if skill in found_skills:

            matched.append(skill)

        else:

            missing.append(skill)

    score = (len(matched) / len(required_skills)) * 100

    return round(score,2), matched, missing


# ----------------------------------
# Streamlit UI
# ----------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload Resume PDF and get Job Match Score"
)


uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)


selected_role = st.selectbox(

    "Select Target Job Role",

    list(job_roles.keys())

)


if uploaded_file is not None:

    text = extract_text(uploaded_file)

    found_skills = extract_skills(text)

    required_skills = job_roles[selected_role]


    score, matched, missing = calculate_score(

        found_skills,
        required_skills

    )


    st.subheader("Detected Skills")

    show_skill_list(found_skills, "No known skills were detected in this resume.")


    st.subheader("Job Match Score")

    st.metric(

        label="Match Score",

        value=f"{score}%"

    )


    st.subheader("Matched Skills")

    show_skill_list(matched, "No required skills matched this resume.")


    st.subheader("Missing Skills")

    show_skill_list(missing, "No required skills are missing.")


    st.subheader("Recommendations")


    if len(missing) > 0:

        st.warning(

            "Improve your resume by learning:\n\n"

            + ", ".join(missing)

        )

    else:

        st.success(

            "Excellent! Your resume matches the selected role."

        )

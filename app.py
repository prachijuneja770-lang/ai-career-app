import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="AI Hiring Assistant")
st.title("🤖 AI Hiring Assistant")

genai.configure(api_key="TUMHARI_API_KEY_YAHAN")

# ---------- STEP 1: Resume Parser ----------
st.header("Step 1: Resume Parser")
uploaded_file = st.file_uploader("Resume PDF upload karo", type="pdf")

resume_text = ""
if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in doc:
        resume_text = resume_text + page.get_text()
    st.success("Resume padh liya!")
    st.write(resume_text[:800])
# ---------- STEP 2: Job Description Analyzer ----------
st.header("Step 2: Job Description Analyzer")
jd_text = st.text_area("Job Description yahan paste karo:", "We need Python, SQL, Machine Learning expert...")

if st.button("Skills Nikalo 🔍"):
    # Simple logic: JD me se common skills dhundo
    common_skills = ["python", "sql", "machine learning", "java", "excel", "communication"]
    found_skills = []
    for skill in common_skills:
        if skill.lower() in jd_text.lower():
            found_skills.append(skill)
    
    if found_skills:
        st.success(f"JD me ye skills mili: {', '.join(found_skills)}")
    else:
        st.warning("Koi skill nahi mili, JD aur bada likho.")
 # ---------- STEP 3: Resume-Job Matching ----------
st.header("Step 3: Resume-Job Match Score")

if st.button("Match Score Nikalo 📊"):
    if resume_text == "":
        st.warning("Pehle Step 1 me Resume upload karo!")
    else:
        # JD wali skills ko resume me dhundo
        common_skills = ["python", "sql", "machine learning", "java", "excel", "communication"]
        jd_skills = [s for s in common_skills if s in jd_text.lower()]
        resume_skills = [s for s in common_skills if s in resume_text.lower()]
        
        matched = set(jd_skills) & set(resume_skills)
        
        if len(jd_skills) > 0:
            score = len(matched) / len(jd_skills) * 100
            st.success(f"Match Score: {score:.1f}%")
            st.write(f"JD skills: {jd_skills}")
            st.write(f"Resume me mili skills: {list(matched)}")
            st.progress(int(score))
        else:
            st.warning("Pehle JD me se skills nikalo.")
# ---------- STEP 4: Bias Detector ----------
st.header("Step 4: Bias Detector")
st.write("Ye JD me biased words check karega")

if st.button("Bias Check Karo ⚖️"):
    biased_words = ["man", "young", "beautiful", "strong boy", "female only"]
    found_bias = []
    for word in biased_words:
        if word in jd_text.lower():
            found_bias.append(word)
    
    if found_bias:
        st.error(f"Bias mila! Ye words hatayo: {', '.join(found_bias)}")
    else:
        st.success("Koi bias nahi mila, JD fair hai! ✅")
   
st.divider()
# ---------- STEP 5: Candidate Ranking ----------
st.header("Step 5: Candidate Ranking")
st.write("Top candidates ki list")

if st.button("Ranking Dikhao 🏆"):
    candidates = [
        {"name": "Rahul", "skills": ["python", "sql", "machine learning"]},
        {"name": "Priya", "skills": ["python", "communication", "excel"]},
        {"name": "Amit", "skills": ["java", "sql"]}
    ]

    jd_skills = ["python", "sql", "machine learning", "communication"]

    scores = []
    for c in candidates:
        matched = len(set(c["skills"]) & set(jd_skills))
        score = matched / len(jd_skills) * 100
        scores.append((c["name"], score))

    # Sort zyada se kam
    scores.sort(key=lambda x: x[1], reverse=True)

    st.success("Final Ranking:")
    for i, (name, score) in enumerate(scores, 1):
        st.write(f"{i}. {name} - {score:.1f}%")
        st.progress(int(score))

# ---------- STEP 6: Interview Question Generator ----------
st.header("Step 6: AI Interview Questions")
job_role = st.text_input("Job Role:", "Python Developer")
skills = st.text_area("Skills:", "Python, SQL")

if st.button("Interview Questions Banao ✨"):
    prompt = f"Generate 5 interview questions for {job_role} with skills {skills}"
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        st.write(response.text)
    except:
        st.success("Demo Mode me jawab:")
        st.info(f"1. {skills} me aapka experience kya hai?\n2. {job_role} ke liye aapne kaunsa project banaya?\n3. Mushkil problem kaise solve karte ho?\n4. Team work ka experience batao?\n5. Aap company me kya value add karoge?")
# ---------- STEP 7: Recruiter Dashboard ----------
st.header("Step 7: Recruiter Dashboard")
st.write("Sab candidates ka final summary")

if st.button("Dashboard Dikhao 📋"):
    import pandas as pd
    
    data = [
        {"Candidate": "Rahul", "Match Score": "75%", "Skills": "Python, SQL, ML", "Missing Skills": "Communication", "Status": "Shortlisted ✅"},
        {"Candidate": "Priya", "Match Score": "50%", "Skills": "Python, Communication", "Missing Skills": "SQL, ML", "Status": "On Hold ⏳"},
        {"Candidate": "Amit", "Match Score": "25%", "Skills": "Java, SQL", "Missing Skills": "Python, ML", "Status": "Rejected ❌"},
    ]
    
    df = pd.DataFrame(data)
    st.table(df)
    st.success("Dashboard ready! HR ko sab clear dikhega.")        
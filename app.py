import streamlit as st
import os
import sqlite3
import pdfplumber
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DB_FOLDER = "database"
RESUME_DATASET_FOLDER = "Resume Dataset"
DB_PATH = os.path.join(DB_FOLDER, "resumes.db")

# Ensure necessary folders exist
for folder in [DB_FOLDER, RESUME_DATASET_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        file_path TEXT, 
        text TEXT, 
        upload_date TEXT, 
        job_role TEXT
    )
''')
conn.commit()

def extract_text_from_pdf(file):
    """Extracts text from a PDF file using pdfplumber."""
    try:
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        if not text.strip():
            raise ValueError("No extractable text found. The PDF may be image-based or corrupted.")
        return text.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"

def rank_resumes(job_description, resumes):
    """Ranks resumes based on similarity to the job description using TF-IDF."""
    try:
        documents = [job_description] + resumes
        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform(documents).toarray()
        job_description_vector = vectors[0]
        resume_vectors = vectors[1:]
        similarities = cosine_similarity([job_description_vector], resume_vectors).flatten()
        return similarities
    except Exception as e:
        st.error(f"TF-IDF Processing Error: {e}")
        return [0] * len(resumes)

def get_all_resumes():
    """Retrieves all resumes from the database and dataset folder."""
    resumes = {}

    # Check resumes in dataset folder
    for file in os.listdir(RESUME_DATASET_FOLDER):
        file_path = os.path.join(RESUME_DATASET_FOLDER, file)
        if file.endswith(".pdf"):
            try:
                with open(file_path, "rb") as f:
                    text = extract_text_from_pdf(f)
                resumes[file] = (text, file_path)
            except Exception as e:
                st.error(f"Error processing {file}: {e}")

    # Check resumes in the database
    c.execute("SELECT name, text, file_path FROM resumes")
    db_resumes = c.fetchall()
    for name, text, file_path in db_resumes:
        if name not in resumes:
            resumes[name] = (text, file_path)

    return resumes

def clean_database():
    """Removes database entries for missing files."""
    c.execute("SELECT id, name, file_path FROM resumes")
    resumes = c.fetchall()
    
    deleted_count = 0
    for resume_id, name, file_path in resumes:
        if not os.path.exists(file_path):  # If file does not exist
            c.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
            conn.commit()
            deleted_count += 1

    if deleted_count > 0:
        st.success(f"🗑️ Removed {deleted_count} missing resumes from database!")
    else:
        st.info("✅ All records are valid, no missing files found.")

def main():
    st.title("🚀 AI Resume Matcher with Database & Resume Dataset")

    st.subheader("📂 Upload Resumes")
    uploaded_files = st.file_uploader("Upload PDF Resumes", type=["pdf"], accept_multiple_files=True)
    job_role = st.text_input("Enter Job Role (Optional)")

    uploaded_resume_texts = []
    uploaded_resume_names = []
    uploaded_resume_paths = []

    if uploaded_files:
        for uploaded_file in uploaded_files:
            resume_text = extract_text_from_pdf(uploaded_file)
            resume_path = os.path.join(RESUME_DATASET_FOLDER, uploaded_file.name)
            
            with open(resume_path, "wb") as f:
                f.write(uploaded_file.read())

            upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute(
                "INSERT INTO resumes (name, file_path, text, upload_date, job_role) VALUES (?, ?, ?, ?, ?)", 
                (uploaded_file.name, resume_path, resume_text, upload_date, job_role)
            )
            conn.commit()

            uploaded_resume_texts.append(resume_text)
            uploaded_resume_names.append(uploaded_file.name)
            uploaded_resume_paths.append(resume_path)

        st.success(f"✅ {len(uploaded_files)} resumes uploaded & added to dataset!")

    st.subheader("💼 Enter Job Description")
    job_description = st.text_area("Paste the job description here")

    if st.button("🔍 Find Best Matches"):
        all_resumes = get_all_resumes()

        for i in range(len(uploaded_resume_names)):
            all_resumes[uploaded_resume_names[i]] = (uploaded_resume_texts[i], uploaded_resume_paths[i])

        if all_resumes:
            names = list(all_resumes.keys())
            resume_texts = [all_resumes[name][0] for name in names]
            file_paths = [all_resumes[name][1] for name in names]
            
            similarities = rank_resumes(job_description, resume_texts)
            sorted_indices = similarities.argsort()[::-1]
            
            top_matches = []
            seen_names = set()
            for idx in sorted_indices:
                if names[idx] not in seen_names:
                    seen_names.add(names[idx])
                    top_matches.append((names[idx], similarities[idx] * 100, file_paths[idx]))
                if len(top_matches) == 3:
                    break
            
            st.subheader("🏆 Top 3 Matching Resumes")
            for idx, (name, match, path) in enumerate(top_matches):
                if os.path.exists(path):  # ✅ Check if file exists before opening
                    with open(path, "rb") as file:
                        st.download_button(
                            label=f"📥 Download {name} ({match:.2f}% match)",
                            data=file,
                            file_name=name,
                            mime="application/pdf",
                            key=f"download_{idx}"
                        )
                else:
                    st.error(f"⚠ File '{name}' not found. It may have been deleted or moved.")

            if uploaded_resume_names:
                st.subheader("📊 Uploaded Resume Scores")
                for i in range(len(uploaded_resume_names)):
                    score = similarities[names.index(uploaded_resume_names[i])] * 100
                    st.write(f"✅ {uploaded_resume_names[i]}: **{score:.2f}% match**")
        else:
            st.warning("⚠ No resumes found!")

    # Button to clean database of missing resumes
    if st.button("🗑️ Clean Missing Resumes from Database"):
        clean_database()

if __name__ == "__main__":
    main()

# 🏆 AI-powered Resume Screening and Ranking System

An AI-driven resume screening and ranking system that matches resumes with job descriptions using **Natural Language Processing (NLP)**. This tool extracts text from PDF resumes, stores them in a database, and ranks them based on similarity to job descriptions.

## 🚀 Features

- 📂 **Resume Upload:** Upload multiple PDF resumes.
- 💄 **Database Integration:** Stores resumes in an SQLite database.
- 🖍 **Text Extraction:** Extracts resume text using `pdfplumber`.
- 🔍 **AI Ranking:** Uses **TF-IDF** and **Cosine Similarity** to rank resumes based on job descriptions.
- 📊 **Top Match Selection:** Highlights the best-matching resumes.
- 📅 **Download Option:** Allows users to download ranked resumes.
- 🗑 **Database Cleanup:** Removes entries of missing files.

## 🛠 Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend:** Python (`sqlite3`, `pdfplumber`)
- **AI/ML:** Scikit-learn (`TfidfVectorizer`, `cosine_similarity`)

## 📞 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Dharmik0712/AI-powered-Resume-Screening-and-Ranking-System.git
   cd AI-powered-Resume-Screening-and-Ranking-System
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## 📝 Usage

1. **Upload Resumes**  
   - Click on "Upload PDF Resumes" and select multiple resumes.
   - Resumes are stored in the **database** and **Resume Dataset folder**.

2. **Enter Job Description**  
   - Paste a job description into the input box.

3. **Find Best Matches**  
   - Click "🔍 Find Best Matches" to rank resumes.
   - The system displays the **Top 3 Matching Resumes** with download options.

4. **Database Cleanup**  
   - Click "🗑 Clean Missing Resumes from Database" to remove invalid entries.

## 🌐 Deployed Link

[Click here to access the deployed app](https://ai-powered-resume-screening-and-ranking-system-cbp4knwoahmpcgf.streamlit.app/)

## 📂 Project Structure

```
📁 AI-powered-Resume-Screening-and-Ranking-System
️️️️️️️️️️️️️️️️️️️️️️️️
📁 database/          # SQLite database files
📁 Resume Dataset/    # Uploaded resumes
📄 app.py            # Main Streamlit app
📄 requirements.txt   # Dependencies
📄 README.md          # Documentation
```

## 🤖 How It Works

1. **Extracts text** from PDF resumes using `pdfplumber`.
2. **Stores** resumes in an SQLite database with job roles.
3. **Uses TF-IDF Vectorization** to convert text into numerical vectors.
4. **Calculates similarity scores** with **cosine similarity**.
5. **Ranks resumes** based on the highest similarity scores.

## ⚡ Future Improvements

- ✅ Add support for **image-based PDF OCR**.
- ✅ Enhance ranking with **deep learning (BERT, GPT)**.
- ✅ Add **multi-user authentication**.

## 🏆 Contributing

Want to improve this project? Contributions are welcome! Feel free to fork and submit a pull request.

## 🐝 License

This project is licensed under the **MIT License**.

---

💡 **Developed by [Dharmik0712](https://github.com/Dharmik0712)**  
🚀 AI meets Resume Screening!


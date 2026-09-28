# 🤖 AI Resume Scanner and Job Prediction System

An AI-powered web application that analyzes resumes, evaluates their suitability for a job description, extracts technical skills, calculates ATS-style scores, and recommends relevant **jobs and internships** using live job data from the Adzuna API.

The system combines **Machine Learning, NLP-based resume analysis, skill matching, job recommendation, and AI assistance** into a single web application.

---

## 🚀 Features

### 📄 AI Resume Scanner

Upload a resume in PDF/TXT format and analyze it automatically.

The system can:

* Parse resume content
* Extract technical skills
* Identify relevant experience
* Analyze education
* Detect projects
* Analyze soft skills
* Generate resume evidence
* Calculate an overall resume score
* Provide criterion-level reasoning

---

### 📊 ATS Resume Analysis

The application generates an ATS-style score based on the resume and the selected job requirements.

The analysis can evaluate areas such as:

* Technical skills
* Experience
* Education
* Projects
* Soft skills

Each criterion includes:

* Score
* Weight
* Strength
* Evidence from the resume
* Reasoning

The final result provides an overall resume-analysis score.

---

## 🎯 Resume ↔ Job Match Score

The recommendation system calculates how closely a resume matches each retrieved job or internship.

The matching process:

1. Extracts skills from the resume.
2. Extracts technical skills from the job description.
3. Normalizes skill names and aliases.
4. Compares resume skills with job requirements.
5. Identifies matched skills.
6. Identifies missing skills.
7. Calculates a resume-match percentage.

### Example

```text
Resume Skills:
Python
Machine Learning
Pandas
SQL
Flask

Job Requirements:
Python
Machine Learning
SQL
Docker
AWS
```

The system identifies:

```text
Matched Skills:
Python
Machine Learning
SQL

Missing Skills:
Docker
AWS
```

The match score is then calculated from the relationship between the required skills and the skills demonstrated by the resume.

This means the displayed match percentage is based on **job-specific requirements**, rather than simply assigning a high score to every job.

---

## 💼 Job & Internship Recommendations

The system supports both:

### Regular Jobs

Examples:

* AI Engineer
* Machine Learning Engineer
* Data Scientist
* Data Analyst
* Python Developer
* Software Engineer
* Data Engineer
* Web Developer

### Internships

Examples:

* AI/ML Internship
* Machine Learning Internship
* Data Science Internship
* Python Internship
* Software Engineering Internship
* Data Analyst Internship

The system automatically searches for opportunities based on the predicted/selected role and resume skills.

---

## 🔎 Live Job Data — Adzuna API

The application integrates with the **Adzuna Jobs API** to retrieve current job and internship listings.

The system uses information such as:

* Job title
* Company
* Location
* Salary/stipend
* Job type
* Description
* Required skills
* Application URL
* Posting date

The recommendations are filtered and ranked based on resume-job compatibility.

---

## 🧠 Job Prediction & Recommendation

The application uses resume information to determine relevant career roles and then searches for matching opportunities.

The recommendation pipeline is approximately:

```text
Resume
   ↓
Resume Parsing
   ↓
Skill Extraction
   ↓
Resume Analysis
   ↓
Role / Job Prediction
   ↓
Adzuna Job Search
   ↓
Job & Internship Filtering
   ↓
Resume ↔ Job Matching
   ↓
Missing Skill Detection
   ↓
Match-based Ranking
   ↓
Recommended Opportunities
```

---

## 📈 Selection Chance Indicator

The application also provides a **resume/job compatibility indicator** based on the calculated resume match and matched-vs-missing skills.

It is intended as an estimate of compatibility, **not a guaranteed probability of being hired**.

The system categorizes the result into:

```text
High Match
Good Match
Moderate Match
Low Match
```

---

## 💬 Milo AI Assistant

The project includes **Milo**, an AI-powered assistant designed around career and recruitment-related queries.

Milo can assist with topics such as:

* Jobs
* Internships
* Companies
* Career opportunities
* Resume-related questions
* Job recommendations

---

## 🛠️ Technology Stack

### Backend

* Python
* Flask
* REST APIs

### Machine Learning

* Scikit-learn
* Machine Learning classification
* Resume classification
* Skill extraction

### NLP / Resume Processing

* NLP-based text processing
* Resume parsing
* Keyword extraction
* Skill normalization
* Resume-job matching

### Frontend

* HTML5
* CSS3
* JavaScript
* Responsive UI
* Animated dashboard interface

### APIs

* Adzuna Jobs API
* Environment-based API configuration

### Database

* SQLite / project database layer

---

## 📁 Project Structure

```text
AI-Resume-Scanner-and-Job-Prediction-System/
│
├── app.py
├── chatbot.py
├── database.py
├── train_model.py
├── test_adzuna.py
├── requirements.txt
├── README.md
│
├── models/
│   ├── resume_classifier.pkl
│   └── vectorizer.pkl
│
├── utils/
│   ├── ats_score.py
│   ├── chatbot.py
│   ├── github_analyzer.py
│   ├── portfolio_analyzer.py
│   ├── prediction_engine.py
│   ├── recommendation.py
│   ├── resume_parser.py
│   ├── skill_extractor.py
│   └── url_extractor.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── templates/
    ├── dashboard.html
    ├── index.html
    ├── login.html
    ├── milo.html
    ├── milo_widget.html
    ├── recommendations.html
    ├── result.html
    ├── test.html
    └── upload.html
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/lithik-raj/AI-Resume-Scanner-and-Job-Prediction-System.git
```

```bash
cd AI-Resume-Scanner-and-Job-Prediction-System
```

---

### 2. Create a virtual environment

```bash
python -m venv env
```

Activate it on Windows:

```powershell
env\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 API Configuration

Create a `.env` file in the project root:

```env
ADZUNA_APP_ID="2d7164f6"
ADZUNA_APP_KEY="662b732b9f9e8a682b15059d91b81613"
```
The project already uses environment variables for API credentials.

---

## ▶️ Run the Application

Vercel : ## 🚀 Live Demo

🔗 **Live Application:** https://ai-resume-scanner-and-job-prediction-system-3xmzp9tjo.vercel.app

The AI Resume Scanner and Job Prediction System is deployed on Vercel and available online for testing.


## 🔄 Application Workflow
## Application Workflow

```text
┌──────────────────────────────┐
│       📄 Upload Resume       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      🔍 Resume Parsing       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      🧠 Skill Extraction     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        📊 ATS Analysis       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      🤖 ML Role Prediction   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      🌐 Adzuna API Search    │
└──────────────┬───────────────┘
               │
               ▼
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌───────────────┐  ┌──────────────────┐
│ 💼 Live Jobs  │  │ 🎓 Internships   │
└───────┬───────┘  └────────┬─────────┘
        │                   │
        ▼                   ▼
┌───────────────┐  ┌────────────────────┐
│ Resume ↔ Job  │  │ Resume ↔ Internship│
│    Matching   │  │      Matching      │
└───────┬───────┘  └──────────┬─────────┘
        │                     │
        ▼                     ▼
┌───────────────┐  ┌────────────────────┐
│ Recommended   │  │ Recommended        │
│     Jobs      │  │   Internships      │
└───────┬───────┘  └──────────┬─────────┘
        │                     │
        └──────────┬──────────┘
                   ▼
        ┌────────────────────────┐
        │ 📈 Match Score &       │
        │    Analysis Results    │
        └───────────┬────────────┘
                    │
                    ▼
        ┌────────────────────────┐
        │ 🤖 Milo Career         │
        │       Assistant        │
        └────────────────────────┘
```

## 📌 Important Notes

* Resume-job matching is an automated compatibility estimate.
* Match percentages depend on the skills detected in the resume and the requirements detected from each job description.
* Job availability depends on the external Adzuna API.
* Salary information may not be available for every listing.
* Selection chance is an estimated compatibility indicator and should not be interpreted as a guaranteed hiring probability.
* API credentials should always remain private.

---

## 🎓 Project Use Case

This project can be used by:

* Students
* Fresh graduates
* Job seekers
* Internship seekers
* Career guidance platforms
* Placement training systems
* Resume screening workflows

It is particularly useful for students who want to understand **which roles match their current skills and which skills they may need to improve**.

---

## 👨‍💻 Author

**Lithik Raj B G**

B.Tech — Artificial Intelligence & Data Science

GitHub:
https://github.com/lithik-raj

Project Repository:
https://github.com/lithik-raj/AI-Resume-Scanner-and-Job-Prediction-System

Vercel :
ai-resume-scanner-and-job-prediction-system-prqmoti12.vercel.app
---

## 📄 License

This project is intended for educational, portfolio, and demonstration purposes.

```

This version specifically documents the **internship functionality** and explains **where the resume-match score comes from** without claiming that it is a guaranteed hiring prediction.
```

# 🎯 AI Resume-JD Matcher

An NLP-powered tool that semantically scores resumes against job descriptions, identifies keyword gaps, and provides actionable feedback — built with **Sentence-BERT**, **FastAPI**, and **React**.

🔗 **Live Demo:** [resume-jd-matcher-ui.onrender.com](https://resume-jd-matcher-ui.onrender.com)  
⚙️ **API:** [praveen5001-resume-jd-matcher.hf.space](https://praveen5001-resume-jd-matcher.hf.space)

---

## 📌 Features

- 📄 Upload resume as **PDF** or **DOCX**
- 📋 Paste any **Job Description**
- 🤖 Semantic scoring using **Sentence-BERT (all-MiniLM-L6-v2)**
- 🔑 Keyword gap analysis with **matching** and **missing** keywords
- 💡 Actionable feedback to improve your resume
- ⚡ Real-time results with a clean, modern UI

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **NLP Model** | Sentence-BERT (all-MiniLM-L6-v2) |
| **Similarity** | Cosine Similarity (scikit-learn) |
| **Backend** | FastAPI + Uvicorn |
| **PDF Parsing** | pdfplumber |
| **DOCX Parsing** | python-docx |
| **Frontend** | React.js + Axios |
| **Styling** | Custom CSS |
| **Backend Deploy** | Hugging Face Spaces (Docker) |
| **Frontend Deploy** | Render (Static Site) |

---

## 🏗️ Project Structure

```
resume-jd-matcher/
├── backend/
│   ├── main.py          # FastAPI app & routes
│   ├── matcher.py       # S-BERT model & scoring logic
│   ├── parser.py        # PDF/DOCX text extraction
│   ├── Dockerfile       # HuggingFace Spaces deployment
│   ├── requirements.txt
│   └── README.md        # HuggingFace Space config
├── frontend/
│   ├── src/
│   │   ├── App.js       # Main React component
│   │   └── App.css      # Styling
│   └── package.json
└── README.md
```

---

## 🚀 How It Works

1. User uploads a **resume** (PDF/DOCX) and pastes a **job description**
2. Backend extracts text from the resume using `pdfplumber` / `python-docx`
3. Both texts are encoded into embeddings using **Sentence-BERT**
4. **Cosine similarity** between embeddings gives the semantic score
5. **Keyword extraction** identifies matching and missing skills
6. A **combined score** (60% semantic + 40% keyword overlap) is returned
7. Frontend displays the score, feedback, and keyword breakdown

---

## 📊 Scoring Formula

```
Combined Score = (0.6 × Semantic Score) + (0.4 × Keyword Overlap Score)
```

| Score Range | Result |
|---|---|
| 75% and above | Strong Match ✅ |
| 55% – 74% | Good Match 🟡 |
| 35% – 54% | Moderate Match 🟠 |
| Below 35% | Low Match 🔴 |

---

## 🖥️ Running Locally

### Prerequisites
- Python 3.11+
- Node.js 18+

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload
```

API runs at: `http://127.0.0.1:8000`  
Swagger docs: `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm start
```

Frontend runs at: `http://localhost:3000`

> Make sure to update the API URL in `frontend/src/App.js` to `http://127.0.0.1:8000` for local development.

---

## 🌐 Deployment

| Service | Platform | URL |
|---|---|---|
| Backend API | Hugging Face Spaces (Docker) | [praveen5001-resume-jd-matcher.hf.space](https://praveen5001-resume-jd-matcher.hf.space) |
| Frontend UI | Render Static Site | [resume-jd-matcher-ui.onrender.com](https://resume-jd-matcher-ui.onrender.com) |

---

## 📸 Screenshot

> Upload your resume → Paste JD → Get your match score instantly!

---

## 👨‍💻 Authors

**Praveen Dangi**  
🔗 [GitHub](https://github.com/Praveen9440) | 

**SHAIK IMRAN**
🔗 [GitHub](https://github.com/shaikimran354) | 

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

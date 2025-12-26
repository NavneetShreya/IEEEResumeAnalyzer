# IEEE Resume Analyzer 🎓

An ML-powered service that parses resumes, analyzes them against job descriptions, and generates quantitative similarity scores to help the IEEE HR team rank candidates efficiently and objectively.

## 🎯 Features

- **PDF Resume Parsing**: Extracts text from PDF resumes using PyPDF2
- **Intelligent Skill Extraction**: Advanced algorithm that handles multiple resume formats
- **Job Description Analysis**: Extracts required skills from job descriptions
- **Similarity Scoring**: Uses cosine similarity to calculate match percentage
- **REST API**: FastAPI endpoint for easy integration



## 🚀 Quick Start

### 1. Install Dependencies

```bash

# Install required packages
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
cd api
uvicorn main:app --reload --port 8000
```

The server will start at: `http://127.0.0.1:8000`


## 📡 API Usage

### Endpoint
```
POST http://127.0.0.1:8000/analyze_resume
```

### Request Parameters
- `resume` (file): PDF resume file
- `job_description` (text): Job description as string

### Example Request (Python)

```python
import requests

url = "http://127.0.0.1:8000/analyze_resume"

# Prepare data
with open("resume.pdf", "rb") as f:
    files = {"resume": f}
    data = {"job_description": "Python, JavaScript, React, AWS..."}
    
    # Send request
    response = requests.post(url, files=files, data=data)
    result = response.json()
    
print(f"Similarity Score: {result['similarity_score']}%")
```

### Response Format

```json
{
  "resume_skills": ["css", "javascript", "react", "java", ...],
  "jd_skills": ["Python", "JavaScript", "React", "AWS", ...],
  "matching_skills": ["javascript", "react", ...],
  "similarity_score": 28.97
}
```

## 📁 Project Structure

```
IEEEResumeAnalyzer/
├── api/
│   └── main.py              # FastAPI application
├── resume_analyzer.py       # Core parsing and analysis logic
├── requirements.txt        # Python dependencies
├── resume.pdf              # Sample resume for testing
├── jd.text                 # Job description file
└── README.md               # This file
```

## 🛠️ Tech Stack

- **PyPDF2**: PDF text extraction
- **FastAPI**: REST API framework
- **Uvicorn**: ASGI server
- **scikit-learn**: Cosine similarity calculation
- **Python 3.13**: Programming language

## 👥 Team Contributions

### API Creation Team ✅
**Aditya Raj**
- FastAPI application setup
- File upload handling
- Response formatting
- Error handling

### Text Extraction & Similarity Team ✅
**Anurag Mishra**
- PDF text extraction
- Advanced skill extraction algorithm
- Similarity calculation
- Matching logic implementation

## 🎓 How It Works

1. **PDF Parsing**: Upload a resume (PDF format)
2. **Text Extraction**: Extract raw text from PDF using PyPDF2
3. **Skill Extraction**: Parse skills from both resume and job description
   - Handles multiple formats: brackets, bullets, pipe-separated
   - Pattern-based fallback for 50+ technologies
4. **Similarity Calculation**: 
   - Convert skills to vectors using CountVectorizer
   - Calculate cosine similarity
   - Return percentage match
5. **Response**: JSON with all skills and similarity score

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/analyze_resume` | Analyze resume vs JD |

## 🔍 Example Output

```
🎯 SIMILARITY SCORE: 88.97%

📝 RESUME SKILLS (12 found):
  1. Figma
  2. css
  3. javascript
  4. react
  5. Java
  ...

📋 JOB DESCRIPTION SKILLS (23 found):
  1. Python
  2. JavaScript
  3. React
  4. AWS
  ...

✨ MATCHING SKILLS (19 matches):
  1. css
  2. javascript
  3. react
  ...
```

## 🚀 Future Enhancements

- [ ] SpaCy integration for advanced NLP
- [ ] Cloud deployment
- [ ] Batch processing for multiple resumes
- [ ] Weighted skill matching
- [ ] PDF report generation

## 📄 License

IEEE Student Chapter Project

---

**Status**: ✅ Fully Functional |

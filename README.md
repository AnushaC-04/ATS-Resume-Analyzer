# ResumeLens AI — Intelligent Resume ATS Analyzer

> **Understand your resume. Match the right opportunity. Improve your chances.**

ResumeLens AI is an AI-powered resume analysis application that compares a candidate's resume against a given job description and provides an ATS-style compatibility analysis.

The application accepts a resume in PDF format and a job description, processes the resume using NLP and semantic search techniques, and uses Google Gemini to generate a structured analysis including an ATS match score, matching skills, missing skills, and content improvement suggestions.

---

## Features

* Upload a resume in PDF format
* Paste a job description
* Extract resume text using PyPDFLoader
* Normalize and clean resume text
* Tokenize, remove stop words, and lemmatize text using spaCy
* Split resume content into smaller chunks
* Generate semantic embeddings using Hugging Face Sentence Transformers
* Store resume chunks using FAISS
* Perform semantic similarity search against the job description
* Retrieve the most relevant resume sections
* Generate an AI-based ATS score from 0–100
* Identify matching skills
* Identify missing skills
* Provide resume content improvement suggestions
* Display results through an interactive Streamlit interface

---

## How It Works

The application follows an NLP + semantic retrieval + Generative AI pipeline:

```text
Resume PDF
     ↓
PDF Text Extraction
     ↓
Text Normalization
     ↓
Tokenization & Lemmatization
     ↓
Text Chunking
     ↓
Hugging Face Embeddings
     ↓
FAISS Vector Database
     ↓
Similarity Search using Job Description
     ↓
Top Relevant Resume Chunks
     ↓
Google Gemini
     ↓
ATS Analysis
     ↓
Streamlit Results
```

---

## Project Structure

```text
ResumeLens-AI/
│
├── app.py
├── analyzer.py
├── README.md
├── requirements.txt
└── .gitignore
```

### `analyzer.py`

Contains the core resume analysis pipeline:

* PDF loading
* Text normalization
* Contraction expansion
* Tokenization
* Stop-word removal
* Lemmatization
* Text chunking
* Embedding generation
* FAISS vector database creation
* Semantic similarity search
* Gemini-based ATS analysis

### `app.py`

Provides the Streamlit user interface.

The application allows users to:

1. Upload a resume PDF
2. Enter a job description
3. Start the analysis
4. View the ATS match score
5. View matching skills
6. View missing skills
7. View resume improvement suggestions
8. Expand and view the complete AI analysis

---

## Technologies Used

### Programming Language

* Python

### NLP & Resume Processing

* spaCy
* contractions
* PyPDF
* LangChain document loaders

### Semantic Search & Embeddings

* Hugging Face Sentence Transformers
* `all-MiniLM-L6-V2`
* FAISS
* LangChain

### Generative AI

* Google Gemini
* LangChain Google GenAI integration
* LangChain Prompt Templates

### Application Framework

* Streamlit

---

## Resume Analysis Process

### 1. Resume Loading

The uploaded PDF resume is processed using `PyPDFLoader` to extract its text content.

The text from the PDF pages is combined into a single document before further processing.

### 2. Text Normalization

The extracted resume text is normalized by:

* Converting text to lowercase
* Normalizing excessive whitespace
* Expanding contractions
* Removing non-alphanumeric characters

This creates a cleaner text representation for downstream NLP processing.

### 3. Tokenization & Lemmatization

spaCy is used to process the normalized resume text.

The pipeline:

* Tokenizes the resume
* Removes stop words
* Converts words to their base forms using lemmatization

The resulting tokens are combined back into processed text.

### 4. Text Chunking

The processed resume is divided into smaller chunks using LangChain's `RecursiveCharacterTextSplitter`.

Current configuration:

```text
Chunk size: 200
Chunk overlap: 40
```

Chunking allows the application to retrieve specific sections of the resume that are most relevant to the job description.

### 5. Embeddings & Vector Search

Each resume chunk is converted into a semantic vector representation using:

```text
sentence-transformers/all-MiniLM-L6-V2
```

FAISS is then used as the vector database for efficient similarity search.

When a job description is provided, the application searches the vector database and retrieves the top 3 most relevant resume chunks.

### 6. Gemini Analysis

The retrieved resume content and the job description are passed to Google Gemini through a LangChain prompt chain.

The model is instructed to provide:

* ATS score
* Matching skills
* Missing skills
* Content improvements

The prompt also instructs the model not to invent skills or experience that are not present in the resume.

---

## ATS Analysis Output

The application presents the analysis in a structured interface containing:

### ATS Match Score

A score between 0 and 100 representing the estimated alignment between the resume and the job description.

### Matching Skills

Skills and qualifications identified in both the resume and job description.

### Missing Skills

Relevant requirements from the job description that are not sufficiently represented in the retrieved resume content.

### Resume Improvements

Content-focused recommendations that may help improve alignment with the target role.

### Full AI Analysis

Users can expand the complete Gemini-generated analysis for additional details.

---

## Running the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ResumeLens-AI.git
cd ResumeLens-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install the spaCy Language Model

```bash
python -m spacy download en_core_web_sm
```

### 5. Configure the Gemini API Key

Create a `.env` file in the project root:

```text
GOOGLE_GEMINI_API_KEY=your_api_key_here
```

The API key should never be committed to GitHub.

Make sure `.env` is included in `.gitignore`.

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Example Workflow

```text
1. Upload Resume
        ↓
2. Paste Job Description
        ↓
3. Click "Analyze my resume"
        ↓
4. Resume Processing
        ↓
5. Semantic Retrieval
        ↓
6. Gemini Analysis
        ↓
7. View ATS Score
        ↓
8. Review Matching & Missing Skills
        ↓
9. Apply Improvement Suggestions
```

---

## Example Use Case

A candidate applying for a Data Analyst position can upload their resume and paste the target job description.

ResumeLens AI can analyze the available resume content and identify:

```text
ATS Match Score
     ↓
Matching Skills
- Python
- SQL
- Pandas
- NumPy
- Power BI

Missing Skills
- Advanced SQL
- Tableau
- Data Visualization

Improvement Suggestions
- Highlight relevant analytical projects
- Strengthen job-specific technical keywords
- Add measurable project outcomes
```

The exact results depend on the resume and job description provided by the user.

---

## Privacy

ResumeLens AI processes the uploaded resume temporarily during analysis.

The application does not intentionally persist the uploaded PDF after processing.

Users should still avoid uploading resumes containing sensitive information when using applications connected to external AI services.

---

## Important Note

The ATS score generated by ResumeLens AI is an **AI-based matching estimate**.

It is not an official score generated by a company's Applicant Tracking System.

The purpose of the application is to help candidates identify potential gaps between their resume and a target job description.

---

## Future Improvements

Potential improvements include:

* More structured ATS scoring methodology
* Section-wise resume analysis
* Improved skill extraction
* Job requirement categorization
* Keyword coverage analysis
* Experience and education matching
* Resume section recommendations
* Support for additional resume formats
* Resume rewriting suggestions
* Job description summarization
* Public deployment
* Improved visualization of ATS results

---

## Project Highlights

This project demonstrates practical implementation of:

* Natural Language Processing
* Text preprocessing
* Semantic embeddings
* Vector databases
* Retrieval-based systems
* Retrieval-Augmented Generation concepts
* Prompt engineering
* Large Language Model integration
* Streamlit application development

---

## Author

**Anusha**

B.Tech Information Technology — 2026 Graduate

---

## Project

**ResumeLens AI — Intelligent Resume ATS Analyzer**

Built with Python, Streamlit, LangChain, FAISS, Hugging Face Sentence Transformers, spaCy, and Google Gemini.

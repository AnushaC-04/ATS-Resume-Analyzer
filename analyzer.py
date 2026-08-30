import os
import re
import contractions
import spacy
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


def load_resume(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    data = "\n".join(
        document.page_content
        for document in documents
    )
    return data

def normalize_text(data):

    data = data.lower()
    data = re.sub(r'\s{2,}', ' ', data)
    data = contractions.fix(data)
    data = re.sub(r'[^0-9a-z\s]', '', data)
    return data

def tokenize_text(data):

    nlp = spacy.load('en_core_web_sm')
    tokens = nlp(data)

    updated_tokens = []
    for token in tokens:
        if not token.is_stop:
            updated_tokens.append(token.lemma_)

    data = ' '.join(updated_tokens).strip()
    return data


def create_chunks(data):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=40
    )
    chunks = text_splitter.create_documents([data])
    return chunks

def create_vector_database(chunks):

    embedding_model = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-V2'
    )

    vector_db = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    return vector_db

def r_search(vector_db, query, k=3):

    retrieved_chunks = vector_db.similarity_search(query,k=k)
    return retrieved_chunks

ats_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
        You are a resume ATS analyzer.

        Analyze the resume against the job description.

        Calculate an ATS score from 0 to 100 based on
        how well the resume matches the required and
        preferred skills.

        Also provide:

        1. Matching skills
        2. Missing skills
        3. Content improvements that could improve
           the ATS score

        Do not invent skills or experience that are
        not present in the resume.

        Give the result in a clear and structured format.
        """
    ),

    (
        "human",
        """
        Resume:

        {resume}

        Job Description:

        {job_description}
        """
    )

])

llm_model = ChatGoogleGenerativeAI(

    model="gemini-3.5-flash",
    api_key=os.environ['GOOGLE_GEMINI_API_KEY']
)

parser = StrOutputParser()
ats_chain = ats_prompt | llm_model | parser

def analyze_resume(file_path, job_description):

    data = load_resume(file_path)
    data = normalize_text(data)
    data = tokenize_text(data)
    chunks = create_chunks(data)
    vector_db = create_vector_database(chunks)

    retrieved_chunks = r_search(
        vector_db,
        job_description,
        k=3
    )

    resume_text = "\n".join(
        chunk.page_content
        for chunk in retrieved_chunks
    )

    response = ats_chain.invoke({"resume": resume_text,"job_description": job_description})
    return response
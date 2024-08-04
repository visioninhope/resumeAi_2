# services/job_description_formatter.py

from pymilvus import Milvus, DataType, CollectionSchema, FieldSchema
from langchain_together.embeddings import TogetherEmbeddings
from dotenv import load_dotenv
import os
from langchain_together import ChatTogether
from langchain import globals
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Milvus
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def load_and_process_documents():
    # Load environment variables
    load_dotenv()
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

    # Set debugging and verbosity
    globals.set_debug(True)
    globals.set_verbose(True)

    # Initialize the TogetherEmbeddings with a specific model
    embeddings = TogetherEmbeddings(
        model="togethercomputer/m2-bert-80M-8k-retrieval", 
        together_api_key=TOGETHER_API_KEY
    )

    # Load the unstructured job descriptions
    loader = TextLoader("./jobdescription.txt")
    documents = loader.load()

    # Define the extraction prompt template
    extraction_prompt = PromptTemplate(
    template="""
    You are an assistant tasked with structuring a complex job description into a well-organized format. Analyze the provided job description, identify and differentiate between required qualifications, preferred qualifications, optional elements, and alternatives. Ensure all relevant details are captured and clearly distinguished.

    Job Description: {document}

    Structured Job Description:
    - **Job Title:** (Extract the job title)
    - **Required Qualifications:** (List all required qualifications, mention any alternatives explicitly)
        - **Education:** (Specifically mention any alternatives or equivalents)
        - **Experience:** (Detail years of experience and areas, noting any optional or alternative experiences)
        - **Skills:** (Specify required skills, noting any optional or alternative skills)
        - **Programming Languages:** (Detail mandatory and optional languages)
        - **Frameworks:** (List required frameworks, specify if alternatives are acceptable)
        - **Databases:** (Mention required databases knowledge)
        - **Cloud Platforms:** (Specify required platforms and if others are acceptable)
        - **Certifications:** (List necessary certifications, mention if they are optional or alternatives exist)
    - **Preferred Qualifications:** (List qualifications that are not mandatory but preferred)
    - **Other Requirements:** (Detail other necessary criteria, e.g., security screenings, noting if they are optional or have alternatives)
    - **Job Responsibilities:** (Clearly outline responsibilities, noting optional or additional tasks)
    - **Overview of Role and Team:** (Provide a brief description of the role's importance and the team's mission)
    - **Important Keywords for ATS:** (List important keywords that might help in ATS optimization)
    """,
    input_variables=["document"],
    )

    # Initialize the language model for extraction
    llm_extractor = ChatTogether(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        temperature=0.8,
        max_tokens=1000,
        together_api_key=TOGETHER_API_KEY,
        streaming=False
    )

    # Create an extraction chain
    extraction_chain = extraction_prompt | llm_extractor | StrOutputParser()

    # Process each document to structure it
    structured_documents = []
    for doc in documents:
        structured_info = extraction_chain.invoke({"document": doc.page_content})
        structured_documents.append(structured_info)

    # Convert structured descriptions into vectors and store them in Milvus
    vector_db = Milvus.from_texts(
        structured_documents,
        embeddings,
        collection_name="job_description_after_formatting",
        connection_args={"host": "127.0.0.1", "port": "19530"},
    )
    return vector_db


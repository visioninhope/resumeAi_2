# services/job_description_formatter.py
from pymilvus import Milvus, DataType, CollectionSchema, FieldSchema,Collection
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


def check_collection_exists(collection_name):
    try:
        collection = Collection(collection_name)
        return True
    except Exception as e:
        return False
 
def process_profile(collection_name):
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

    # Load the profile information from a text file
    loader = TextLoader("./profile.txt")
    profile_documents = loader.load()

    # Define the extraction prompt template
    extraction_prompt = PromptTemplate(
    template="""
    You are an assistant tasked with formatting a professional profile into a structured format suitable for resume building. Analyze the provided profile, categorize and format it into relevant sections.

    Profile Information: {document}

    Structured Profile:
    - **About Me:** (Provide a brief personal introduction)
    - **Skills:** (List technical and soft skills)
    - **Programming Languages:** (List programming languages known)
    - **Frameworks:** (List all frameworks experienced with)
    - **Databases:** (List all databases mentioned)
    - **Cloud Platforms:** (Specify any cloud platforms known)
    - **Certifications:** (List relevant certifications)
    - **Educational Background:** (Provide details about education)
    - **Professional Experience:** (Summarize work experience)
    - **Achievements:** (Highlight significant achievements)
    -**total years of **Professional experience**
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

    # Process each profile document to structure it
    structured_profiles = []
    for profile in profile_documents:
        structured_info = extraction_chain.invoke({"document": profile.page_content})
        structured_profiles.append(structured_info)

    # Convert structured profiles into vectors and store them in Milvus in a different collection
    vector_db = Milvus.from_texts(
        structured_profiles,
        embeddings,
        collection_name=collection_name,
        connection_args={"host": "127.0.0.1", "port": "19530"},
    )
    return vector_db


from pymilvus import Milvus, DataType, CollectionSchema, FieldSchema,MilvusClient
from langchain_together.embeddings import TogetherEmbeddings
from dotenv import load_dotenv
import os
from langchain_together import ChatTogether
from langchain import globals
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Milvus
from langchain_core.documents import Document
from langchain_community.vectorstores import Milvus
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser



TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# set_debug(True) -enables detailed debugging output for troubleshooting, 
# set_verbose(True)- increases the verbosity of general runtime messages for more informative logging.
globals.set_debug(True)
globals.set_verbose(True)
load_dotenv()
# Initialize Milvus client


# Initialize the TogetherEmbeddings with a specific model
embeddings = TogetherEmbeddings(
    model="togethercomputer/m2-bert-80M-8k-retrieval", 
    together_api_key = TOGETHER_API_KEY
)

loader = TextLoader("./jobdescription.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=30)
docs = text_splitter.split_documents(documents)



# Here's how you can create a new collection

vector_db = Milvus.from_documents(
    docs,
    embeddings,
    collection_name="jobdescription",
    connection_args={"host": "127.0.0.1", "port": "19530"},
)

# query = "who is bakugou in my hero academia?"
# docs = vector_db.similarity_search(query)
retriever = vector_db.as_retriever()

# print("retriever", retriever)

### Retrieval Grader 
llm = ChatTogether(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    temperature=0.8,  # Slightly higher to introduce a bit of variability
    max_tokens=1000,  # Limit the length of each output to keep summaries concise
    timeout=None,  # Keep as is unless you have specific timing constraints
    max_retries=2,  # Suitable for most cases
    presence_penalty=0.3,  # Helps discourage repetition of the same information
    frequency_penalty=0.2,  # Reduces the likelihood of repeating the same phrases
    top_p=0.9,  # Encourages a wider range of responses
    together_api_key=TOGETHER_API_KEY,
    streaming=False  # Set to true if needed for real-time applications
)

prompt = PromptTemplate(
    template="""You are a grader assessing relevance 
    of a retrieved document to a user question. If the document contains keywords related to the user question, 
    grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals. 
    
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.
    Provide the binary score as a JSON with a single key 'score' and no premable or explaination.
     
    Here is the retrieved document: 
    {document}
    
    Here is the user question: 
    {question}
    """,
    input_variables=["question", "document"],
)

retrieval_grader = prompt | llm | JsonOutputParser()

# question = "who is Bakugou"
# docs = retriever.invoke(question)
# doc_txt = docs[1].page_content
# print(retrieval_grader.invoke({"question": question, "document": doc_txt}))


### Generate

from langchain.prompts import PromptTemplate
from langchain import hub
from langchain_core.output_parsers import StrOutputParser

prompt = PromptTemplate(
    template="""You are an assistant tasked with extracting specific information from job descriptions. Analyze the provided job description, and list out the required skills, experience, and programming languages. Ensure all relevant details are captured even if not explicitly labeled under conventional headings:
    
    Job Description: {document}
    Extracted Information:
    - **Skills:**
        - List all the skills mentioned, including both technical and soft skills.
    - **Programming Languages:**
        - Programming Languages mentioned.
    -**Frameworks:**
        - Frameworks mentioned.
    - **Databases:**
        - Databases mentioned.
    - **Cloud Platforms:**
        - Cloud Platforms mentioned.
    - **Experience:**
        - Mention the required years of experience.
    - **Education:**
        - Mention the required level of education.
    - **job responsibilities:**
        - Mention the job responsibilities
    - **job title:**
        - Mention the job title
    - **Certifications:**
        - Certifications mentioned.
    - **Other Requirements:**
        - Any other requirements mentioned.
    -**List important keywords from ATS Prespective: **
    """,
    input_variables=["document"],
)





# Chain
rag_chain = prompt | llm | StrOutputParser()

# print ("docs", docs)
# Run
generation = rag_chain.invoke({"document": docs})

# print("generation", generation)

vector_db = Milvus.from_texts(
    generation,
    embeddings,
    collection_name="jobdescription_aftergeneration",
    connection_args={"host": "127.0.0.1", "port": "19530"},
)






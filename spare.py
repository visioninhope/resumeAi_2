
# And here is how you retrieve that stored collection
# vector_db = Milvus(
#     embeddings,
#     connection_args={"host": "127.0.0.1", "port": "19530"},
#     collection_name="myhero",
# )
# query = "who is bakugou in my hero academia?"
# docs = vector_db.similarity_search(query)



# print(docs[0].page_content)


# from langchain_together import Together

# llm = Together(
#     model="codellama/CodeLlama-70b-Python-hf",
#     together_api_key=TOGETHER_API_KEY,
# )

# print(llm.ainvoke("who is bakuogu in my hero academia?"))


# chat = ChatTogether(
#     model="meta-llama/Llama-3-70b-chat-hf",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     together_api_key=TOGETHER_API_KEY,
#     )


# # Create a collection in Milvus (if not exists)
# collection_name = "milvus_demo"

# # 1. Create schema
# # schema = MilvusClient.create_schema(
# #     auto_id=False,
# #     enable_dynamic_field=False,
# # )

# # # 2. Add fields to schema
# # schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)
# # schema.add_field(field_name="my_vector", datatype=DataType.FLOAT_VECTOR, dim=5)

# # schema = CollectionSchema(fields)
# # client.create_collection(collection_name, schema)

# # Embedding documents
# docs = [
#     "my hero academia is a popular anime.",
#     "midoriya is the main character of my hero academia.",
#     "Bakugo is a student in class 1-A.",
#     "All Might is the number one hero.",
#     "Endeavor is the number two hero.",
#     "Shoto Todoroki is the son of Endeavor.",
#     "Deku is the nickname of Midoriya.",
#     "One For All is a powerful quirk.",
# ]

# text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#     # Set a really small chunk size, just to show.
#     chunk_size=20,
#     chunk_overlap=5,
#     # length_function=len,
#     # is_separator_regex=False,  
#     model_name='text-embedding-3-small',
#     encoding_name='text-embedding-3-small',
# )

# texts = text_splitter.create_documents(docs)
# # print("Texts:", texts)
# # Extracting page_content from each Document object to form a list of strings
# texts = [doc.page_content for doc in texts]
# # print("Texts:", texts)

# documents = [Document(page_content=text) for text in texts]


# vectorstore = Milvus.from_documents(
#     documents=documents,
#     collection_name=collection_name,
#     embedding=embeddings.embed_documents(texts),
#     connection_args={"uri": "./milvus_demo.db"},
#     drop_old=True,  # Drop the old Milvus collection if it exists

# )



# # Convert the vectorstore to a retriever
# retriever = vectorstore.as_retriever()

# from langchain.prompts import PromptTemplate
# from langchain_core.output_parsers import JsonOutputParser


# from langchain_together import ChatTogether

# # choose from our 50+ models here: https://docs.together.ai/docs/inference-models
# llm = ChatTogether(
#     # together_api_key="YOUR_API_KEY",
#     model="meta-llama/Llama-3-70b-chat-hf",
# )

# prompt = PromptTemplate(
#     template="""You are a grader assessing relevance 
#     of a retrieved document to a user question. If the document contains keywords related to the user question, 
#     grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals. 
    
#     Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.
#     Provide the binary score as a JSON with a single key 'score' and no premable or explaination.
     
#     Here is the retrieved document: 
#     {document}
    
#     Here is the user question: 
#     {question}
#     """,
#     input_variables=["question", "document"],
# )


# retrieval_grader = prompt | llm | JsonOutputParser()
# question = "agent memory"
# docs = retriever.invoke(question)
# doc_txt = docs[1].page_content
# print(retrieval_grader.invoke({"question": question, "document": doc_txt}))



    # Example of retrieving all entries from a collection called 'job_description_after_formatting'
    # try:
    #     results = client.query(
    #         collection_name="job_description_after_formatting",
    #         filter="",  # Assuming no specific filter is required to fetch all data
    #         output_fields=["*"],  # Fetch all fields; adjust if vector fields or specific fields are needed
    #         limit=100,  # Limit to 100 results; adjust as needed
    #         timeout=30  # Timeout after 30 seconds; adjust as needed
    #     )
    #     for result in results:
    #         print(result)  # This will print each document's data returned by the query
    # except Exception as ex:
    #     print(f"An error occurred: {ex}")


    # # Example of retrieving all entries from a collection called 'profile_after_formatting'
    # try:
    #     results = client.query(
    #         collection_name="job_description_after_formatting",
    #         filter="",  # Assuming no specific filter is required to fetch all data
    #         output_fields=["*"],  # Fetch all fields; adjust if vector fields or specific fields are needed
    #         limit=100,  # Limit to 100 results; adjust as needed
    #         timeout=30  # Timeout after 30 seconds; adjust as needed
    #     )
    #     for result in results:
    #         print(result)  # This will print each document's data returned by the query
    # except Exception as ex:
    #     print(f"An error occurred: {ex}")